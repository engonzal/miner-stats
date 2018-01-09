# miner-stats
Send GPU mining API stats to InfluxDB (ewbf and optiminer)

## Setup
On any devices, let's get a python environment setup.

Ubuntu:
```bash
sudo apt-get install python3 python3-virtualenv
virtualenv -p /usr/bin/python3 miner-stats
cd miner-stats
source bin/activate
git clone git@github.com:engonzal/miner-stats.git
cd miner-stats
pip install -r requirements.txt
```

## Usage
```bash
# optiminer
python miner-stats.py -h miner-hostname -a 6000 -i influxhost -r 8086 -u root -p influxpassword -d databasename -m optiminer

#ewbf
python miner-stats.py -h miner-hostname -a 6000 -i influxhost -r 8086 -u root -p influxpassword -d databasename -m ewbf
```

### Parameters
```bash
Usage: miner-stats.py [OPTIONS]

Options:
  -h, --host TEXT            Hostname running ewbf
  -a, --port TEXT            port to communicate with api on
  -i, --influxhost TEXT      hostname of influxdb server
  -r, --influxport TEXT      port influx is running on
  -u, --influxuser TEXT      influx database user account
  -p, --influxpassword TEXT  influx database password
  -d, --influxdatabase TEXT  influx database to write to
  -m, --miner TEXT           app miner
  --help                     Show this message and exit.
  ```
