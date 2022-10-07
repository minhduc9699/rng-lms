import requests
from datetime import datetime
from env.config import Config
from .query_template import query_template


def get_metrics(query):
  PROMETHEUS_API = Config.get().sentry.prometheus
  res = requests.get(f'{PROMETHEUS_API}/query', params={'query': query})
  payload = res.json()
  return payload['data']

def get_vps_metrics(node_exporter, vps_name):
  vps_metrics = []
  for key, query in query_template.items():
    metrics = get_metrics(query.substitute(node_exporter=node_exporter, vps_name=vps_name))
    metrics_value = metrics['result'][0]['value']
    vps_metrics = [*vps_metrics, {
      'label': key,
      'timestamp': datetime.fromtimestamp(metrics_value[0]).strftime('%Y-%m-%d:%H:%M:%S'),
      'value': str(round(float(metrics_value[1]))) + '%'
    }]
  return vps_metrics
    
