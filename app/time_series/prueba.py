from models import *
import pandas as pd

data = pd.read_csv('data.csv')

t = TimeSeries('a',min_date='01/01/2023',max_date='28/02/2023',data=data,plot=True)

t.create_TLP()

t.plot_clusters()
