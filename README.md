# General

### BCS API Swagger

Schema: http://embeddedcc.github.io/api-docs/swagger.yaml

UI: http://embeddedcc.github.io/api-docs/#/

### Local Grafana Access

Runs on: ` http://localhost:3000/`

Default login and password: `admin:admin`

### InfluxDB Terminal
Enter terminal: `influx`

Examples:
```
> CREATE DATABASE junk
> USE junk
> SELECT * FROM "outputs"
> SELECT * FROM "temperatures"
> DROP DATABASE junk
```

# Mac

### InfluxDB Installation

`brew install influxdb`

### InfluxDB Run

`influxd`

### Grafana Installation

https://grafana.com/docs/installation/mac/

`brew install grafana`

### Grafana run

Only once: `brew tap homebrew/services`

`brew services start grafana`

# Ubuntu

### InfluxDB Installation

https://docs.influxdata.com/influxdb/v1.7/introduction/installation/

```
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/lsb-release
echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
```

```
sudo apt-get update && sudo apt-get install influxdb
```

### InfluxDB Run

```
sudo service influxdb start
```

### Grafana Installation

https://grafana.com/docs/installation/debian/
```
curl https://packages.grafana.com/gpg.key | sudo apt-key add -
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
sudo apt-get update && sudo apt-get install grafana
```

### Grafana run

```
sudo service grafana-server start
```

# TODO
- setup.py
  - daemon entry point
  - dependencies
- dockerfile
- logger class
- use env vars instead of constants
- dockstrings you slacker
