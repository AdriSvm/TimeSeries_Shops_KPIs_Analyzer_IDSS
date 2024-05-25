import datetime
import logging
import os

from scipy.cluster._optimal_leaf_ordering import squareform
from sklearn.preprocessing import StandardScaler
from sqlalchemy.orm import Session, joinedload
from app.models import Cliente, TiquetCabecera, TiquetLinea
import pandas as pd
import numpy as np
from tslearn.preprocessing import TimeSeriesScalerMinMax, TimeSeriesScalerMeanVariance
from tslearn.utils import to_time_series_dataset
from sqlalchemy import func, text
from tslearn.utils import to_time_series_dataset
from tslearn.metrics import cdist_dtw
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import matplotlib.pyplot as plt


class TimeSeries:
    def __init__(self, sql_session: Session, min_date: str, max_date: str,data:pd.DataFrame=pd.DataFrame(),plot:bool=False):
        self.logger = logging.getLogger(__name__)
        self.sql_session = sql_session
        self.min_date = min_date
        self.max_date = max_date
        self.plot = plot
        self.max_d = None
        if data.empty:
            data = TimeSeries.load_clients(datetime.datetime.strptime(self.min_date,'%d/%m/%Y'),datetime.datetime.strptime(self.max_date,'%d/%m/%Y'))
        if data.empty:
            self.logger.debug(f"Data empty, getting clients...")
            self.clients = self.get_clients()
            self.logger.info(f'Clients obtained, len: {len(self.clients)}')
            self.data = self.process_clients()
            self.logger.info(f"Clients processed, len: {len(self.data)}")
            if self.data.empty:
                raise Exception('No data to process')
        else:
            self.logger.debug(f"Data not empty")
            self.data = data
        self.logger.debug(f"Processing time series")
        self.time_series = self.process_time_series()
        if type(self.time_series) is bool or self.time_series.empty:
            raise Exception('No time series data to process')

    @staticmethod
    def load_clients(start_date,end_date,folder_path:str='data'):
        logger = logging.getLogger(__name__)
        logger.debug(f"Loading clients from {folder_path}")

        data_frame = pd.DataFrame()


        for filename in os.listdir(folder_path):
            if filename.startswith('timeseriesdata_') and filename.endswith('.csv'):

                try:
                    parts = filename.split('_')
                    file_start_date = datetime.datetime.strptime(parts[1], '%Y-%m-%d')
                    file_end_date = datetime.datetime.strptime(parts[2].replace('.csv', ''), '%Y-%m-%d')


                    if file_start_date <= start_date and file_end_date >= end_date:
                        file_path = os.path.join(folder_path, filename)
                        df = pd.read_csv(file_path)
                        data_frame = df
                        break
                except Exception as e:
                    print(f"Error procesando el archivo {filename}: {e}")

        # Combinar los DataFrames cargados
        if not data_frame.empty:
            data_frame['fechaalta'] = pd.to_datetime(data_frame['fechaalta'],format='%Y-%m-%d')
            data_frame = data_frame[
                (data_frame['fechaalta'] >= start_date) & (data_frame['fechaalta'] <= end_date)]

        return data_frame

    def get_clients(self):
        return self.sql_session.query(Cliente). \
            options(joinedload(Cliente.tiquets)). \
            filter(
            func.convert(text('date'), Cliente.fldFechaAlta, text('103')) >= func.convert(text("date"),
                                                                                          self.min_date.strftime(
                                                                                              '%d/%m/%Y'), text(
                    "103")) if self.min_date else True,

            func.convert(text('date'), Cliente.fldFechaAlta, text('103')) <= func.convert(text("date"),
                                                                                          self.max_date.strftime(
                                                                                              '%d/%m/%Y'),
                                                                                          text(
                                                                                              "103")) if self.max_date else True
        ).all()

    def __preprocess_data(self, data):
        data = data.dropna()
        data = data.drop_duplicates()
        self.logger.debug(f"Data dropped na and duplicates")
        data.replace('SR', 'HOMBRE')
        data.replace('SRA', 'MUJER')
        self.logger.debug(f"Genre replaced")
        fecha_valid = lambda x: x if len(x.split('/')) == 3 and len(x) == 10 and (x.split('/')[0]).isdigit() and int(
            x.split('/')[0]) < 32 and (x.split('/')[1]).isdigit() and int(x.split('/')[1]) < 13 and (
                                         x.split('/')[2]).isdigit() and len(x.split('/')[2]) == 4 else 0
        genero_valid = lambda x: x if x in ['HOMBRE', 'MUJER'] else 0
        data = data[data['fechaalta'].apply(fecha_valid) != 0]
        data = data[data['aniversario'].apply(fecha_valid) != 0]
        data = data[data['genero'].apply(genero_valid) != 0]
        data = data[data['visitasPos'].apply(lambda x: x if x >= 0 else 0) != 0]
        data = data[data['fechabaja'].apply(lambda x: x if not x else 0) != 0]
        self.logger.debug(f"Prepro funcs applied")

        return data

    def __feature_extraction(self, data):
        self.logger.debug(f"starting feature extraction...")
        data['TM'] = (data['importePos'] + data['importeNeg']) / (data['visitasPos'] + abs(data['visitasNeg']))
        data['TM'] = data['TM'].replace(np.inf, 0)
        data['PD'] = (-data['prendasNeg']) / (data['prendasPos'] - data['prendasNeg'])
        data['PD'] = data['PD'].replace(np.inf, 1)
        data['UPT'] = (data['prendasPos'] + abs(data['prendasNeg'])) / (data['visitasPos'] + abs(data['visitasNeg']))
        data['UPT'] = data['UPT'].replace(np.inf, 0)
        data['PVM'] = (data['importePos'] + data['importeNeg']) / (data['prendasPos'] + abs(data['prendasNeg']))
        data['PVM'] = data['PVM'].replace(np.inf, 0)
        data['fechaalta'] = pd.to_datetime(data['fechaalta'], format='%d/%m/%Y')
        data['CMV'] = (data['importePos'] + data['importeNeg']) / ((
                                                                           datetime.datetime.now() - data[
                                                                       'fechaalta']).dt.days / 30.44)
        data['cl_registrados'] = data.groupby('fechaalta')['fechaalta'].transform('count')
        self.logger.debug(f"Feature extraction finished")
        return data

    def process_clients(self) -> pd.DataFrame:
        if not self.clients:
            return pd.DataFrame()
        self.logger.debug(f"processing clients")

        data = pd.DataFrame(columns=['idcliente', 'canal', 'codpostal', 'poblacion', 'provincia', 'pais', 'genero',
                                     'fechaalta', 'fechabaja', 'aniversario', 'visitasPos', 'prendasPos', 'importePos',
                                     'visitasNeg', 'prendasNeg', 'importeNeg'])
        for i, client in enumerate(self.clients):
            visitasPos = len([_ for _ in client.tiquets if _.fldImporteNeto > 0])
            visitasNeg = len([_ for _ in client.tiquets if _.fldImporteNeto < 0])
            prendasPos = sum([t.fldPrendas for t in client.tiquets if t.fldImporteNeto > 0])
            prendasNeg = sum([t.fldPrendas for t in client.tiquets if t.fldImporteNeto < 0])
            importePos = sum([t.fldImporteNeto for t in client.tiquets if t.fldImporteNeto > 0])
            importeNeg = sum([t.fldImporteNeto for t in client.tiquets if t.fldImporteNeto < 0])

            data.loc[len(data)] = [client.fldIdCliente, client.fldIdAlmacen, client.fldCodPostal, client.fldPoblacion,
                                   client.fldProvincia, client.fldPais, client.fldTipoNombre.upper(),
                                   client.fldFechaAlta, client.fldFechaBaja, client.fldAniversario, visitasPos,
                                   prendasPos, importePos,
                                   visitasNeg, prendasNeg, importeNeg]
        self.logger.debug(f"Main economic data calculated and data created")

        data = self.__preprocess_data(data)
        data = self.__feature_extraction(data)
        data.to_csv(f'data/timeseriesdata_{datetime.datetime.strptime(self.min_date,"%d/%m/%Y").strftime("%Y-%m-%d")}_{datetime.datetime.strptime(self.max_date,"%d/%m/%Y").strftime("%Y-%m-%d")}.csv')
        self.logger.debug(f"data saved to csv")
        return data

    def process_time_series(self):
        if type(self.data) is bool:
            return False

        self.logger.debug(f"starting processing time series")

        relevant_columns = ['fechaalta', 'TM', 'UPT', 'CMV', 'PVM', 'PD', 'cl_registrados']

        for column in relevant_columns:
            if column not in ('PD','fechaalta'):
                self.data = self.remove_outliers_iqr(self.data, column)

        # Step 2: Aggregate the data by date
        grouped_data = self.data[relevant_columns].groupby('fechaalta').agg({
            'TM': 'mean',
            'UPT': 'mean',
            'CMV': 'mean',
            'PVM': 'mean',
            'PD': 'mean',
            'cl_registrados': lambda x: x.iloc[0]
        }).reset_index()

        scaler = TimeSeriesScalerMeanVariance()
        time_series_data = grouped_data[['TM', 'UPT', 'CMV', 'PVM', 'PD']].values
        normalized_data = scaler.fit_transform(time_series_data)

        nan_mask = np.isnan(normalized_data).any(axis=(1, 2))
        print("Number of samples with NaNs in normalized data:", nan_mask.sum())

        normalized_data_clean = normalized_data[~nan_mask]

        # Drop corresponding rows in grouped data
        grouped_data = grouped_data[~nan_mask].reset_index(drop=True)

        # Reshape the normalized data
        normalized_data_clean = normalized_data_clean.reshape(
            (normalized_data_clean.shape[0], normalized_data_clean.shape[1], 1))

        # Step 3: Compute the DTW distance matrix
        dtw_distance_matrix = cdist_dtw(normalized_data_clean)

        # Step 4: Perform hierarchical clustering
        linked = linkage(squareform(dtw_distance_matrix), method='ward')

        if self.plot:
            plt.figure(figsize=(10, 7))
            dendrogram(linked)
            plt.title('Dendrogram')
            plt.xlabel('Sample index')
            plt.ylabel('Distance')
            plt.show()

        last = linked[-10:, 2]
        acceleration = np.diff(last, 2)
        acceleration_rev = acceleration[::-1]
        idx = np.argmax(acceleration_rev) + 2

        optimal_max_d = last[::-1][idx]
        self.max_d = optimal_max_d
        print(f"Optimal max_d: {optimal_max_d}")


        clusters = fcluster(linked, optimal_max_d, criterion='distance')


        grouped_data['cluster'] = clusters


        #output_path = 'clustered_time_series_data.csv'
        #grouped_data.to_csv(output_path, index=False)

        if self.plot:
            plt.figure(figsize=(14, 7))
            for column in ['TM', 'UPT', 'CMV', 'PVM', 'PD']:
                plt.plot(grouped_data['fechaalta'], grouped_data[column], label=column)
            plt.xlabel('Date')
            plt.ylabel('Value')
            plt.title('KPIs Over Time')
            plt.legend()
            plt.show()

        return grouped_data


    def create_TLP(self):
        if type(self.time_series) is bool or self.time_series.empty:
            return False


        cluster_means = self.time_series.groupby('cluster')[['TM', 'UPT', 'CMV', 'PVM', 'PD','cl_registrados']].mean()

        # Calcular las medias globales de cada KPI
        global_means = self.time_series[['TM', 'UPT', 'CMV', 'PVM', 'PD','cl_registrados']].mean()

        # Definir umbrales basados en el 10% de la media global
        thresholds = {
            'TM': [global_means['TM'] * 0.9, global_means['TM'] * 1.1],
            'UPT': [global_means['UPT'] * 0.9, global_means['UPT'] * 1.1],
            'CMV': [global_means['CMV'] * 0.9, global_means['CMV'] * 1.1],
            'PVM': [global_means['PVM'] * 0.9, global_means['PVM'] * 1.1],
            'cl_registrados': [global_means['cl_registrados'] * 0.9, global_means['cl_registrados'] * 1.1],
            'PD': [global_means['PD'] * 1.1, global_means['PD'] * 0.9]  # Invertir los umbrales para PD
        }

        def color_traffic_light(value, thresholds, kpi):
            if kpi == 'PD':
                if value < thresholds[1]:  # Umbral inferior
                    return 'green'
                elif value < thresholds[0]:  # Umbral superior
                    return 'yellow'
                else:
                    return 'red'
            else:
                if value > thresholds[1]:  # Umbral superior
                    return 'green'
                elif value > thresholds[0]:  # Umbral inferior
                    return 'yellow'
                else:
                    return 'red'

        # Aplicar colores a cada celda de la tabla de medias
        colored_means = cluster_means.copy()
        for col in cluster_means.columns:
            colored_means[col] = cluster_means[col].apply(color_traffic_light, thresholds=thresholds[col], kpi=col)

        if self.plot:
            # Visualizar la tabla con colores
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.axis('off')

            # Crear tabla de colores
            cell_colors = []
            for i, row in cluster_means.iterrows():
                cell_colors.append([color_traffic_light(value, thresholds[col], col) for col, value in row.items()])

            table = ax.table(cellText=cluster_means.round(2).values,
                             rowLabels=cluster_means.index,
                             colLabels=cluster_means.columns,
                             cellColours=cell_colors,
                             cellLoc='center',
                             loc='center')

            # Ajustar diseño de la tabla
            table.auto_set_font_size(False)
            table.set_fontsize(12)
            table.scale(1.2, 1.2)

            plt.title('Panel de Semáforo para cada Característica y Cluster')
            plt.show()

        return global_means,colored_means


    def plot_clusters(self):
        if type(self.time_series) is bool or self.time_series.empty:
            return False

        fig, ax = plt.subplots(figsize=(14, 7))
        scatter = ax.scatter(self.time_series['fechaalta'], [1] * len(self.time_series), c=self.time_series['cluster'], cmap='viridis', s=50, alpha=0.6,
                             edgecolors='w')

        # Añadir leyenda
        legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
        ax.add_artist(legend1)

        # Añadir títulos y etiquetas
        ax.set_title('Distribución de Fechas por Clusters')
        ax.set_xlabel('Fecha')
        ax.set_yticks([])  # Ocultar el eje y, ya que no es relevante en este caso
        ax.grid(True)

        # Mostrar el gráfico
        plt.show()

    def remove_outliers_iqr(self,data, column):
        """
        Elimina outliers utilizando el método del rango intercuartílico (IQR).

        :param data: DataFrame con la serie temporal.
        :param column: Nombre de la columna a procesar.
        :return: DataFrame sin outliers.
        """
        if data[column].dtype not in ['int64', 'float64']:
            data[column] = data[column].astype('float64')
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        filtered_data = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
        return filtered_data
