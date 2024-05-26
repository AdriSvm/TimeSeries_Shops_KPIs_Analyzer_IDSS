from datetime import datetime,timedelta
import logging

import numpy as np

from app import db
from . import timeseries_bp
from flask import request, jsonify, session, current_app
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from sqlalchemy.orm import Session
from app.models import User, Cliente,TiquetLinea,TiquetCabecera
from .models import TimeSeries,color_traffic_light

@timeseries_bp.route("/get_info/", methods=["POST"])
@jwt_required()
def timeseries_info():
    logger = logging.getLogger(__name__)
    logger.debug(f"Getting timeseries...")

    current_user = get_jwt_identity()

    sql_session = db.session

    user = sql_session.query(User).filter_by(fldIdUsuario=current_user).first()

    min_date = request.json.get('start', None)
    max_date = request.json.get('end', None)

    try:
        min_date1 = datetime.strptime(min_date, '%Y-%m-%d')
        max_date1 = datetime.strptime(max_date, '%Y-%m-%d')
    except ValueError or TypeError as e:
        logger.error(f"Error parsing dates: {e}")
        return jsonify({"message": "Invalid date format"}), 400

    if user.fldIdNivelAcceso == '1111':
        t = TimeSeries(sql_session,min_date,max_date)
    else:
        t = TimeSeries(sql_session,min_date,max_date,idalmacen=user.fldIdAlmacen)

    res = {}
    res['labels'] = [str(x)[:10] for x in t.time_series['fechaalta'].values]


    colors = {1: 'rgba(255, 99, 132, 1)', 2: 'rgba(54, 162, 235, 1)', 3: 'rgba(255, 206, 86, 1)', 4: 'rgba(75, 192, 192, 1)', 5: 'rgba(153, 102, 255, 1)', 6: 'rgba(255, 159, 64, 1)', 7: 'rgba(255, 99, 132, 1)', 8: 'rgba(54, 162, 235, 1)', 9: 'rgba(255, 206, 86, 1)', 10: 'rgba(75, 192, 192, 1)', 11: 'rgba(153, 102, 255, 1)', 12: 'rgba(255, 159, 64, 1)'}
    clusters = [colors.get(int(x),'rgba(255,255,255,1)') for x in t.time_series['cluster'].values[1:]]
    #KPIS colors that must be different from the clusters
    kpis_colors = {'TM': 'rgba(0, 128, 128, 1)','PD':'rgba(128, 0, 128, 1)','UPT':'rgba(0, 255, 127, 1)','CMV':'rgba(255, 20, 147, 1)','PVM':'rgba(0, 0, 139, 1)'}
    cluster_colors = [colors[x] for x in np.sort(t.time_series['cluster'].unique())]
    res['datasets'] = [{'label':var,'data':[str(x) for x in t.time_series[var].values],'backgroundColor':[kpis_colors[var]]+clusters,
                        'borderColor':kpis_colors[var],'borderWidth':1,'radius':6} for var in ('TM','UPT','PD','CMV','PVM')]

    registers = {}
    registers['labels'] = res['labels'].copy()
    registers['datasets'] = [{'label':'cl_registrados','data':[str(x) for x in t.time_series['cl_registrados'].values],'backgroundColor':[kpis_colors['TM']]+clusters,
                        'borderColor':kpis_colors['TM'],'borderWidth':1,'radius':6}]

    global_means,colored_means = t.create_TLP()

    table = [[(str(round((t.time_series[t.time_series['cluster'] == cl])[var].mean(), 2)),
               colored_means.loc[cl][var]) for var in ('TM', 'UPT', 'CMV', 'PVM', 'PD', 'cl_registrados')]
             for cl in np.sort(t.time_series['cluster'].unique())]

    names = [(str(round(global_means[var],2)), var) for var in ('TM', 'UPT', 'CMV', 'PVM', 'PD', 'cl_registrados')]

    final = {'plot': res,'table': table,'first_row':names,'registers_plot':registers,'cluster_colors':cluster_colors}
    sql_session.close()
    return jsonify(final)