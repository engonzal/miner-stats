import json
import requests
from influxdb import InfluxDBClient
import click
import datetime
import time

def minerQuery(host, port, miner):
  if miner in ('ewbf'):
    response = requests.get("http://{}:{}/getstat".format(host, port))
    data = response.json()
  elif miner in ('optiminer'):
    response = requests.get("http://{}:{}".format(host, port))
    data = response.json()
  else:
    print("Unknown miner application, please specify a new one")
    data = 1
  return data

def influxMessage(measurement, host, gpuid, value):
  current_time = datetime.datetime.utcnow().isoformat()
  json_body = [{
  "measurement": measurement,
  "tags": {
    "host": host,
      "gpuid": gpuid
      },
  "time": current_time,
  "fields": {
    "value": int(value)
    }
  }]
  return json_body

def influxSend(message, influx_info):
  client = InfluxDBClient(influx_info['influxhost'], influx_info['influxport'], influx_info['influxuser'], influx_info['influxpassword'], influx_info['influxdatabase'])
  client.write_points(message)
  print(message)

def optiminer(api_data, host, influx_info):
  filter_keys = ["iteration_rate", "os", "share", "stratum", "uptime", "version"]
  for gpu_stat in api_data:
    if gpu_stat not in filter_keys:
      for item in api_data[gpu_stat]:
        if item != 'Total':
          gpuid = item
          for stat in api_data[gpu_stat][item]:
            measurement = "sols_{}".format(stat)
            value = api_data[gpu_stat][item][stat]
            message = influxMessage(measurement, host, gpuid, value)
            influxSend(message, influx_info)
            print(message)
  return message

def ewbf(api_data, host, influx_info):
  filter_keys = ["cudaid", "busid", "name"]
  for gpu_stat in api_data['result']:
    for gpu_value in gpu_stat:
      if gpu_value not in filter_keys:
        gpuid = gpu_stat['gpuid']
        value = gpu_stat[gpu_value]
        message = influxMessage(gpu_value, host, gpuid, value)
        influxSend(message, influx_info)
  return message

@click.command()
@click.option('--host', '-h', help='Hostname running ewbf')
@click.option('--port', '-a', help='port to communicate with api on')
@click.option('--influxhost', '-i', help='hostname of influxdb server')
@click.option('--influxport', '-r', help='port influx is running on')
@click.option('--influxuser', '-u', help='influx database user account')
@click.option('--influxpassword', '-p', help='influx database password')
@click.option('--influxdatabase', '-d', help='influx database to write to')
@click.option('--miner', '-m', help='app miner')
def main(host, port, influxuser, influxpassword, influxhost, influxport, influxdatabase, miner):
  while True:
    api_data = minerQuery(host, port, miner)
    influx_info = dict({"influxhost": influxhost, "influxport": influxport, "influxuser": influxuser, "influxpassword": influxpassword, "influxdatabase": influxdatabase})
    if miner.lower() in ('ewbf'):
      message = ewbf(api_data, host, influx_info)
    elif miner.lower() in ('optiminer'):
      message = optiminer(api_data, host, influx_info)
    time.sleep(int(30))
main()
