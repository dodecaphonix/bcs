# InfluxDB

### Install
`brew install influxdb`
### Start
`influxd`
### Access
`influx`
### Examples
```
> CREATE DATABASE junk
> USE junk
> SELECT * FROM "outputs"
> SELECT * FROM "temperatures"
> DROP DATABASE junk
```

# Grafana

### Install
`brew install grafana`

`brew tap homebrew/services`

### Start
`brew services start grafana`

### Access
` http://localhost:3000/`

admin:password

https://grafana.com/docs/installation/mac/
