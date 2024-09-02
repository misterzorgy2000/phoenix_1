from os import makedirs
import pandas as pd
import datetime

from cow.ai import DS_DATA_DIR
from cow.gnocchi_client import GnocchiClient
from cow import conf

gnocchi = GnocchiClient(conf).client

def get_resource_list(type='prometheus'):
    return gnocchi.resource.list(type)

def save_metrics():
    makedirs(DS_DATA_DIR, exist_ok=True)
    
    metric_cols = conf.CONF.ai.metrics  
    target_cols = conf.CONF.ai.target
        
    prometheus_resources = gnocchi.resource.list('prometheus')
    node_job_resource = list(filter(lambda el: el['job'] == 'node', prometheus_resources))[0]
    resource_id = node_job_resource['id']
    timespan = int(conf.CONF.gnocchi_client.timespan)
    
    start = (datetime.datetime.now() - datetime.timedelta(minutes=timespan)).timestamp()
    end = datetime.datetime.today().timestamp()
    
    for ix, metric_id in enumerate(metric_cols + target_cols):
        temp = gnocchi.metric.get_measures(metric_id, resource_id=resource_id, start=start, end=end)
        df = pd.DataFrame([], columns=['resource_id', 'ts', metric_id])
            
        for ij, measure in enumerate(temp):
            df.loc[ij] = [resource_id, measure[0].timestamp(), measure[2]]
            
        if not ix:
            data = df
        else:
            data = data.merge(df, on=['resource_id', 'ts'], how='inner')

    data.to_csv(f'{DS_DATA_DIR}/data.csv')