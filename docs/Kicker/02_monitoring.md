# Infrastructure Monitoring mit TIG-Stack

## Sinnhaftigkeit der Veränderung des Datenbanksystems

+ Eine Zeitreihendatenbank ist für eine "ewige Tabelle" gut geeignet
+ Infrastructure Monitoring
	+ "In InfluxDB you don’t have to define schemas up front." [^0]
	+ "Relational databases can handle time series data, but are not optimized for common time series workloads." [^0]
	+ "Using predefined rules and thresholds, the monitoring process detects potential issues and generates alerts when threshold breaches occur, thereby helping to maintain system health." [^5]
+ Kombinierte Datenerfassung von Kickertisch und AuVAReS wahrscheinlich möglich

## TIG-Stack Setup auf dem Raspberry Pi 3

Um die Adresse des RPi herauszufinden nutzen wir den Befehl `ip a`. Im Folgenden kann diese IP `localhost` ersetzten.
Wir bringen APT auf den neusten Stand.
```bash
sudo apt update
sudo apt upgrade -y
```
Wir installieren die Services telegraf, influxDB und grafana. [^1], [^'2] 

`influxDB` wird für die vorhandene OS Version heruntergeladen und installiert. Die Datenbank wird über `http://localhost:8086` erreicht.
```bash
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/os-release
echo "deb https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt update && sudo apt install -y influxdb
```
`influxdb` wird durch die folgenden Anweisungen als Service bei jedem boot gestartet.
```bash
sudo systemctl unmask influxdb.service
sudo systemctl start influxdb
sudo systemctl enable influxdb.service

sudo apt install influxdb-client
```
Das gleiche machen wir für `grafana`. Nach der Installation erreichen wir die Oberfläche von `grafana` über `http://localhost:3000`. 
```bash
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
sudo apt update && sudo apt install -y grafana
sudo systemctl unmask grafana-server.service
sudo systemctl start grafana-server
sudo systemctl enable grafana-server.service
```
Wir installieren `telegraf` mit
```bash
sudo apt-get update
sudo apt-get install telegraf
```
Wir konfigurieren `telegraf.conf` mit der Ausgabe `outputs.influxdb` um die Messungen automatisch in eine Datenbank `telegraf` abzuspeichern.
```bash
cd /etc/telegraf
sudo nano telegraf.conf
systemctl start telegraf
```
Um in grafana auf influxDB und telegraf zugreifen zu können legen wir in influxDB entsprechende Nutzer an.
Wir können influxDB mit dem Befehl `influx` aufrufen und die Datenbanken und Messungen im Terminal ausgeben.
```bash
influx

Connected to http://localhost:8086 version 1.6.7~rc0
InfluxDB shell version: 1.6.7~rc0
> create database db01
> use db01
Using database db01
> create user grafana with password '<password>' with all privileges
> grant all privileges on db01 to grafana
> use telegraf
Using database telegraf
> create user telegraf with password '<password>' with all privileges
> exit 
```
Wir können über `HTTP` Werte in die Datenbank schreiben (siehe docs für Syntax [^3]) 
```bash
curl -i -XPOST 'http://localhost:8086/write?db=db01' --data-binary '<measurement>[,<tag-key>=<tag-value>...] <field-key>=<field-value>[,<field2-key>=<field2-value>...] [unix-nano-timestamp]'
```

Wir können die Services mit dem `systemctl stop <telegraf, grafana, influxdb>` beenden oder mit `systemctl restart <telegraf, grafana, influxdb>` neu starten.
In der grafana Oberfläche können wir influxDB als Datenquelle hinzufügen indem wir unter Menüpunkt "Data sources" unsere Datenbank eintragen.
+ Database name: `influxdb-db01`
+ HTTP
    + URL: `http://localhost:8086`
+ InfluxDB Details
    + Database: `db01`
    + User: `grafana`
    + Password: `<password>`

Mit grafana können wir ein Dashboard erstellen, über welches das Gesamtsystem überwacht werden kann.  

# Quellen

#[^1]: https://simonhearne.com/2020/pi-influx-grafana/

#[^2]: https://devconnected.com/how-to-setup-telegraf-influxdb-and-grafana-on-linux/

#[^3]: https://docs.influxdata.com/influxdb/v1/write_protocols/line_protocol_tutorial/

#[^0]: https://docs.influxdata.com/influxdb/v1/concepts/crosswalk/

#[^5]: https://www.influxdata.com/blog/infrastructure-monitoring-basics-telegraf-influxdb-grafana/
