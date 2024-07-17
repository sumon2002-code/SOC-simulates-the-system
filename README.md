# SOC-simulates-the-system
SOC simulation system Uses Rsync file, Message Queue (Kafka...) mechanism to send to the Log receiving system. The Log receiving system includes Elastic Search and GrayLog for processing.
## Prepare the system
|  NAME | OS  |
| ------------ | ------------ |
| SIEM  |   UBUNTU 22.04|
|  WEB SERVER |  UBUNTU 22.04 |
## Installation
### <a/>1. On the SIEM machine
#### 1.1 Download and install elasticsearch
`
  wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.10.2-amd64.deb
`
-  **Download hash to check packet integrity**

`
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.10.2-amd64.deb.sha512
`

- ** Check integrity successfully**

 ![image](https://i.imgur.com/7MrnB1Y.png)

- ** Unpack and install**

`sudo dpkg -i elasticsearch-7.17.22-amd64.deb`

- **Edit elasticsearch configuration file**

`sudo vim /etc/elasticsearch/elasticsearch.yml`

![image](https://i.imgur.com/8LmV2gL.png)

- **Launch elasticsearch**

```bash
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service
```

- **Check if elasticsearch is running or not**

`curl -X GET "localhost:9200/?pretty"`

![image](https://i.imgur.com/sesXaOH.png)

#### 1.2 Install mongoDB

- **Install gnupg**

`sudo apt-get install gnupg curl`

- **import key**

`curl -fsSL https://pgp.mongodb.com/server-6.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor`

- **Create list files for mongoDB**

```bash
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
update apt-get
sudo apt-get update
```

- **Install mongoDB**

`sudo apt-get install -y mongodb-org`

#### 1.3 Install Graylog

- **Download and install graylog server**
```bash
wget https://packages.graylog2.org/repo/packages/graylog-5.2-repository_latest.deb
sudo dpkg -i graylog-5.2-repository_latest.deb
sudo apt-get update && sudo apt-get install graylog-server
```

- **Create password_secret**

`< /dev/urandom tr -dc A-Z-a-z-0-9 | head -c${1:-96};echo;`

![image](https://imgur.com/bLjGD5D.png )

- **Create root_password_sha2**

`echo -n "Enter Password: " && head -1 </dev/stdin | tr -d '\n' | sha256sum | cut -d" " -f1`

![image](https://imgur.com/AN7EBUT.png "image")

- **Enter the above 2 passwords into the configuration file**

`sudo vim /etc/graylog/server/server.conf`

![image](https://imgur.com/IDYdK4N.png "image")

- **Edit web address**

![image](https://imgur.com/763aeoe.png "image")

- **Add address of elasticsearch**

![image](https://imgur.com/6nWolLc.png "image")

- **Run graylog**

```bash
sudo systemctl daemon-reload
sudo systemctl enable graylog-server.service
sudo systemctl start graylog-server.service
```
- **Graylog is already running**

![image](https://imgur.com/e0lT1Y7.png "image")

- **Go to graylog's website using the machine's address and log in with the admin user and the password created from root_password_sha2**

![image](https://imgur.com/hay4YI0.png "image")

#### 1.4 Install Kafka

- **Install jdk**

`sudo apt install openjdk-11-jdk -y`

- **Download kafka**

`wget https://dlcdn.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz`

- **Decompress with command**

`tar -xvf kafka_2.13-3.7.0.tgz`

- **Move to the file you just extracted**

`sudo mv kafka_2.13-3.7.0 /usr/local/kafka`

- **Create systemd file for zookeeper**

`sudo vim  /etc/systemd/system/zookeeper.service`

- **Add information to the file**

```
[Unit]
Description=Apache Zookeeper server
Documentation=http://zookeeper.apache.org
Requires=network.target remote-fs.target
After=network.target remote-fs.target

[Service]
Type=simple
ExecStart=/usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties
ExecStop=/usr/local/kafka/bin/zookeeper-server-stop.sh
Restart=on-abnormal

[Install]
WantedBy=multi-user.target

```

- **Create systemd file for kafka**

`sudo vim /etc/systemd/system/kafka.service`

- **Add information to the file**

```
[Unit] 
Description=Apache Kafka Server
Documentation=http://kafka.apache.org/documentation.html
Requires=zookeeper.service

[Service]
Type=simple
Environment="JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64"
ExecStart=/usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties
ExecStop=/usr/local/kafka/bin/kafka-server-stop.sh

[Install]
WantedBy=multi-user.target

```

- **Run zookeeper and kafka**

```bash
sudo systemctl daemon-reload
systemctl start zookeeper
systemctl start kafka
```

- **Check zookeeper and kafka are running**

![image](https://imgur.com/gBS1FTb.png "image")

![image](https://imgur.com/TAQIRw1.png "image")

- **Create Topic for kafka**

- Go to the kafka folder

`cd /usr/local/kafka `

- Create topic

`bin/kafka-topics.sh --create --topic graylog-input --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1`

- Check to see if there is a topic yet

`bin/kafka-topics.sh --list --bootstrap-server localhost:9092`

- **Create input for graylog to receive log from kafka**

- Go to graylog > system > input > select syslog kafka and select Launch new input

![image](https://imgur.com/kTfr5rk.png "image")

- Fill in the information and press launch input, press start input to begin

![image](https://imgur.com/3oGNV4s.png "image")

- Check if kafka has received a message from kafka

`bin/kafka-console-producer.sh --topic graylog-input --bootstrap-server localhost:9092`

- Go through the search section to check

![image](https://imgur.com/CTrcNzV.png "image")

### <a/>2. On the web server

- **Install GW Nginx to have a web server**

`sudo apt install nginx`

- **Check if the website is working or not**

![image](https://imgur.com/93NITBH.png "image")

- **Website construction**

    **[Website](https://github.com/sumon2002-code/SOC-simulates-the-system/tree/master/Webserver "Web")**

- **Configure GW Nginx and Log Requests**

![Image](https://imgur.com/PeO5KHc.png "Image")
![image](https://imgur.com/31DKUpS.png "image")

- **Install filebeat to get nginx's access log and send it to kafka**

```bash
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.14.1-amd64.deb
sudo dpkg -i filebeat-8.14.1-amd64.deb
```
- **configure filebeat**

`sudo vim /etc/filebeat/filebeat.yml`

![image](https://imgur.com/GUd2OQV.png "image")

- **Edit output section**

![image](https://imgur.com/IUs3YaG.png "image")

- **Run filebeat**

```bash
sudo filebeat modules enable nginx
sudo systemctl enable filebeat
sudo systemctl start filebeat
```

- **Check logbeat status**

![image](https://imgur.com/WOtnS0c.png "image")

- **Check graylog to get the log**

![image](https://imgur.com/LwGCHlR.png "image")

