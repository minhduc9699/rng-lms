import requests
from string import Template
from datetime import datetime
from env.config import Config


def get_metrics(query):
  PROMETHEUS_API = Config.get().sentry.prometheus
  res = requests.get(f'{PROMETHEUS_API}/query', params={'query': query})
  payload = res.json()
  return payload['data']

def get_vps_metrics(node_exporter, vps_name):
  query_template = {
    'cpu': Template('''
      (((count(count(node_cpu_seconds_total {
      instance = "$node_exporter", job = "$vps_name"
      }) by(cpu))) - avg(sum by(mode)(rate(node_cpu_seconds_total {
      mode = "idle", instance = "$node_exporter", job = "$vps_name"
      } [5m15s])))) * 100) / count(count(node_cpu_seconds_total {
      instance = "$node_exporter", job = "$vps_name"
    }) by(cpu))'''),

    'ram': Template('''
      100 - ((node_memory_MemAvailable_bytes {
      instance = "$node_exporter", job = "$vps_name"
      }* 100) / node_memory_MemTotal_bytes {
      instance = "$node_exporter", job = "$vps_name"
      })
    '''),

    'sysload_5m': Template('''
      avg(node_load5 {
      instance = "$node_exporter", job = "$vps_name"
      }) / count(count(node_cpu_seconds_total {
      instance = "$node_exporter", job = "$vps_name"
      }) by(cpu)) * 100
    '''),

    'sysload_15m': Template('''
      avg(node_load15 {
      instance = "$node_exporter", job = "$vps_name"
      }) / count(count(node_cpu_seconds_total {
      instance = "$node_exporter", job = "$vps_name"
      }) by(cpu)) * 100
    '''),

    'swap_used': Template('''      
      ((node_memory_SwapTotal_bytes {
        instance = "$node_exporter", job = "$vps_name"
      } - node_memory_SwapFree_bytes {
        instance = "$node_exporter", job = "$vps_name"
      }) / (node_memory_SwapTotal_bytes {
        instance = "$node_exporter", job = "$vps_name"
      })) * 100
    '''),

    'disk_used': Template('''      
      100 - ((node_filesystem_avail_bytes {
      instance = "$node_exporter", job = "$vps_name", mountpoint = "/", fstype != "rootfs"
      }* 100) / node_filesystem_size_bytes {
      instance = "$node_exporter", job = "$vps_name", mountpoint = "/", fstype != "rootfs"
      })
    '''),
  }
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
    
