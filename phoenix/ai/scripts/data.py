from os import makedirs
import pandas as pd
import datetime

from cow.ai import DS_DATA_DIR
from cow.gnocchi_client import GnocchiClient
from cow import conf

gnocchi = GnocchiClient(conf).client

def get_resource_list(type='prometheus'):
    return gnocchi.resource.list(type)

    """ETL Pipeline
    """
def save_metrics():
    makedirs(DS_DATA_DIR, exist_ok=True)
    
    metric_cols = conf.CONF.ai.metrics  
    target_cols = conf.CONF.ai.target
        
    try:
        prometheus_resources = gnocchi.resource.list('prometheus')
    except Exception:
        print(Exception)
        
    node_job_resource = list(filter(lambda el: el['job'] == 'node', prometheus_resources))[0]
    resource_id = node_job_resource['id']
    timespan = int(conf.CONF.gnocchi_client.timespan)
    
    start = (datetime.datetime.now() - datetime.timedelta(minutes=timespan)).timestamp()
    end = datetime.datetime.today().timestamp()
    
    resources = list(
        filter(
            lambda el: el["job"] in ["node", "scaphandre"]
            and el["instance"].split(":")[0] == "10.1.101.34",
            prometheus_resources,
        )
    )
    
    data = None

    METRIC_MAP = {
        "scaph_host_disk_total_bytes": "Total disk",
        "scaph_host_disk_available_bytes": "Free disk",
        "scaph_host_load_avg_five": "CPU load 5 avg",
        "scaph_host_memory_total_bytes": "Total RAM",
        "scaph_host_memory_free_bytes": "Free RAM",
        "scaph_host_power_microwatts": "Power MW",
        "node_cpu_seconds_total": "CPU seconds",
        "node_hwmon_temp_celsius": "Temperature",
    }

    for resource in resources:
        resource_id = resource["id"]

        for ix, metric_id in enumerate(metric_cols + target_cols):
            if metric_id in resource["metrics"]:
                temp = gnocchi.metric.get_measures(
                    metric_id, resource_id=resource_id, start="2024-09-10"
                )
                df = pd.DataFrame([], columns=["ts", METRIC_MAP[metric_id]])

                for ij, measure in enumerate(temp):
                    df.loc[ij] = [measure[0].timestamp(), measure[2]]

                df.to_csv(f"{DS_DATA_DIR}/metrics/{metric_id}.csv")

                if data is None:
                    data = df
                else:
                    data = data.merge(df, on=["ts"], how="inner")

    prepare_data()         
    
    data.to_csv(f'{DS_DATA_DIR}/data.csv')
    
def prepare_data(data):
    data = data.dropna()
    data["Power Consumption"] = data["Power MW"] / 1000000
    data["Total disk"] = data["Total disk"] / 1000000
    data["Free disk"] = data["Free disk"] / 1000000
    data["Total RAM"] = data["Total RAM"] / 1000000
    data["Free RAM"] = data["Free RAM"] / 1000000

    data["RAM"] = data["Total RAM"] - data["Free RAM"]

    data["Disk"] = data["Total disk"] - data["Free disk"]
    data['Datetime'] = data['ts'].apply(lambda ts: datetime.fromtimestamp(ts).strftime('%H:%M:%S'))
    
    data["Time"] = data['ts'].apply(lambda ts: int("".join(datetime.fromtimestamp(ts).strftime('%H:%M:%S').split(':'))))
    
    return data
    