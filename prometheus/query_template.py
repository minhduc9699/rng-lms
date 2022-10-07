from string import Template

query_template = {
  'CPU': Template('''
      (((count(count(node_cpu_seconds_total {
      instance = "$node_exporter", job = "$vps_name"
      }) by(cpu))) - avg(sum by(mode)(rate(node_cpu_seconds_total {
      mode = "idle", instance = "$node_exporter", job = "$vps_name"
      } [5m15s])))) * 100) / count(count(node_cpu_seconds_total {
      instance = "$node_exporter", job = "$vps_name"
    }) by(cpu))'''),
  'RAM': Template('''
      100 - ((node_memory_MemAvailable_bytes {
      instance = "$node_exporter", job = "$vps_name"
      }* 100) / node_memory_MemTotal_bytes {
      instance = "$node_exporter", job = "$vps_name"
      })
  '''),
  'SYSLOAD_5M': Template('''
      avg(node_load5 {
      instance = "$node_exporter", job = "$vps_name"
      }) / count(count(node_cpu_seconds_total {
      instance = "$node_exporter", job = "$vps_name"
      }) by(cpu)) * 100
  '''),
  'SYSLOAD_15M': Template('''
      avg(node_load15 {
      instance = "$node_exporter", job = "$vps_name"
      }) / count(count(node_cpu_seconds_total {
      instance = "$node_exporter", job = "$vps_name"
      }) by(cpu)) * 100
  '''),
  'SWAP_USED': Template('''      
      ((node_memory_SwapTotal_bytes {
        instance = "$node_exporter", job = "$vps_name"
      } - node_memory_SwapFree_bytes {
        instance = "$node_exporter", job = "$vps_name"
      }) / (node_memory_SwapTotal_bytes {
        instance = "$node_exporter", job = "$vps_name"
      })) * 100
  '''),
  'DISK_USED': Template('''      
      100 - ((node_filesystem_avail_bytes {
      instance = "$node_exporter", job = "$vps_name", mountpoint = "/", fstype != "rootfs"
      }* 100) / node_filesystem_size_bytes {
      instance = "$node_exporter", job = "$vps_name", mountpoint = "/", fstype != "rootfs"
      })
  '''),
}

