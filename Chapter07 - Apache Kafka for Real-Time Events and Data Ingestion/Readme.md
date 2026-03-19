# Chapter 07 - Apache Kafka for Real-Time Events and Data Ingestion


```
$ cd Chapter07/multinode
```

<br/>

```
$ docker compose up -d
```

<br/>

```
$ docker ps
CONTAINER ID   IMAGE                             COMMAND                  CREATED         STATUS         PORTS     NAMES
9d154c46ff2e   confluentinc/cp-kafka:7.6.0       "/etc/confluent/dock…"   2 minutes ago   Up 2 minutes             multinode-kafka-1-1
eeb748d35702   confluentinc/cp-kafka:7.6.0       "/etc/confluent/dock…"   2 minutes ago   Up 2 minutes             multinode-kafka-3-1
d949e54e0ecc   confluentinc/cp-kafka:7.6.0       "/etc/confluent/dock…"   2 minutes ago   Up 2 minutes             multinode-kafka-2-1
7151f56d6d40   confluentinc/cp-zookeeper:7.6.0   "/etc/confluent/dock…"   2 minutes ago   Up 2 minutes             multinode-zookeeper-2-1
d1ab8513b73d   confluentinc/cp-zookeeper:7.6.0   "/etc/confluent/dock…"   2 minutes ago   Up 2 minutes             multinode-zookeeper-3-1
f2936115277b   confluentinc/cp-zookeeper:7.6.0   "/etc/confluent/dock…"   2 minutes ago   Up 2 minutes             multinode-zookeeper-1-1
```

<br/>

```
$ docker logs multinode-kafka-1-1
```

<br/>

```
$ CONTAINER_NAME=multinode-kafka-1-1
$ docker exec -it $CONTAINER_NAME bash
```

<br/>

```
$ BOOTSTRAP_SERVER=localhost:19092
$ TOPIC=mytopic
$ GROUP=mygroup
```

<br/>

```
// OK!
$ kafka-topics --create --bootstrap-server $BOOTSTRAP_SERVER --replication-factor 3 --partitions 3 --topic $TOPIC
```

<br/>

```
// OK!
$ kafka-topics --list --bootstrap-server $BOOTSTRAP_SERVER
```

<br/>

```
// OK!
$ kafka-topics --bootstrap-server $BOOTSTRAP_SERVER --describe --topic $TOPIC
```

<br/>

```
Topic: mytopic	TopicId: FDSRMlR1SGaDzIhi5x2fEQ	PartitionCount: 3	ReplicationFactor: 3	Configs:
	Topic: mytopic	Partition: 0	Leader: 3	Replicas: 3,1,2	Isr: 3,1,2
	Topic: mytopic	Partition: 1	Leader: 1	Replicas: 1,2,3	Isr: 1,2,3
	Topic: mytopic	Partition: 2	Leader: 2	Replicas: 2,3,1	Isr: 2,3,1
```

<br/>

```
$ kafka-console-producer --broker-list $BOOTSTRAP_SERVER --topic $TOPIC
```

```
> Hello!
```

<br/>

**+1 Terminal**

```
$ CONTAINER_NAME=multinode-kafka-1-1
$ docker exec -it $CONTAINER_NAME bash
```

<br/>

```
$ BOOTSTRAP_SERVER=localhost:19092
$ TOPIC=mytopic
```

<br/>

```
// OK!
$ kafka-console-consumer --bootstrap-server $BOOTSTRAP_SERVER --topic $TOPIC --from-beginning
```

<br/>

```
Hello!
```

<br/>

```
$ docker compose down
```

<br/>

### Streaming from a database with Kafka Connect

```
$ cd Chapter07/connect/kafka-connect-custom-image
$ cd kafka-connect-custom-image
$ docker build -t connect-custom:1.0.0 .
$ cd ../
```

<br/>

```
$ vi .env_kafka_connect
```

<br/>

```
$ docker compose up -d
```

<br/>

```
$ export PROJECT_NAME=big_data
$ source ${PYENV_ROOT}/versions/${PROJECT_NAME}-env/bin/activate
```

<br/>

```
// Добавить данные в базу postgres
$ cd simulations
$ pip install -r ./simulations/requirements.txt
$ python simulations/make_fake_data.py

// Завершить спустя какое-то количество
$ ^C
```

<br/>

```
// OK!
$ docker compose exec postgres psql -U postgres -d postgres -c 'SELECT * FROM customers';
$ docker compose exec postgres psql -U postgres -d postgres -c 'SELECT count(*), max(dt_update) FROM customers';
```

<br/>

```
// Создаем топик json-customers
$ docker compose exec broker kafka-topics --create --bootstrap-server localhost:9092 --partitions 2 --replication-factor 1 --topic json-customers
```

<br/>

```
// Удалить, если что-то пошло не так
// curl -X DELETE localhost:8083/connectors/pg-connector-json

// register the connectors
$ curl -X POST -H "Content-Type: application/json" --data @connectors/connect_jdbc_pg_json.config localhost:8083/connectors | jq
```

<br/>

```json
{
  "name": "pg-connector-json",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "true",
    "tasks.max": "1",
    "connection.url": "jdbc:postgresql://postgres:5432/postgres",
    "connection.user": "postgres",
    "connection.password": "postgres",
    "mode": "timestamp",
    "timestamp.column.name": "dt_update",
    "table.whitelist": "customers",
    "topic.prefix": "json-",
    "validate.non.null": "false",
    "poll.interval.ms": "500",
    "db.timezone": "UTC",
    "timestamp.initial": "0",
    "name": "pg-connector-json"
  },
  "tasks": [],
  "type": "source"
}
```

<br/>

```
$ curl -s localhost:8083/connectors | jq
```

<br/>

```
[
  "pg-connector-json"
]
```

<br/>


```
$ curl -s localhost:8083/connectors/pg-connector-json/status | jq
{
  "name": "pg-connector-json",
  "connector": {
    "state": "RUNNING",
    "worker_id": "connect:8083"
  },
  "tasks": [
    {
      "id": 0,
      "state": "RUNNING",
      "worker_id": "connect:8083"
    }
  ],
  "type": "source"
}
```

<br/>

```
$ docker logs connect
```

<br/>

```
// FAIL!
$ docker exec -it broker kafka-console-consumer --bootstrap-server localhost:9092 --topic json-customers --from-beginning
```

<br/>

```
Ничего не появилось!
```


<br/>

```
$ docker compose exec broker kafka-topics --list --bootstrap-server localhost:9092
__consumer_offsets
_schemas
docker-connect-configs
docker-connect-offsets
docker-connect-status
json-customers
```

<br/>

```
// OK!
$ docker compose exec postgres psql -U postgres -d postgres -c "UPDATE customers SET dt_update = NOW();"
```


<br/>

```
Нужно правильно модифицировать connector, т.к. с датами что-то не то.
```

<br/>

```
// Пропустим пока AWS
// $ curl -X POST -H "Content-Type: application/json" --data @connectors/connect_s3_sink.config localhost:8083/connectors
```

<br/>

```
$ docker compose down -v
```

<br/>

### Real-time data processing with Kafka and Spark

<br/>

```
$ spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 processing/consume_from_kafka.py
```

<br/>

```
$ python simulations/make_fake_data.py
```

<br/>

```
// OK!
$ docker compose exec postgres psql -U postgres -d postgres -c "UPDATE customers SET dt_update = NOW();"
```

<br/>

```
-------------------------------------------
Batch: 0
-------------------------------------------
+------+-----+---------------+----------+-------+
|gender|count|first_birthdate| first_now|avg_age|
+------+-----+---------------+----------+-------+
|     F|   15|     1984-11-09|2026-03-20|   55.6|
|     M|   18|     1970-09-25|2026-03-20|  52.17|
+------+-----+---------------+----------+-------+

-------------------------------------------
Batch: 1
-------------------------------------------
+------+-----+---------------+----------+-------+
|gender|count|first_birthdate| first_now|avg_age|
+------+-----+---------------+----------+-------+
|     F|   15|     1984-11-09|2026-03-20|   55.6|
|     M|   19|     1970-09-25|2026-03-20|  54.21|
+------+-----+---------------+----------+-------+

-------------------------------------------
Batch: 2
-------------------------------------------
+------+-----+---------------+----------+-------+
|gender|count|first_birthdate| first_now|avg_age|
+------+-----+---------------+----------+-------+
|     F|   28|     1984-11-09|2026-03-20|  56.21|
|     M|   33|     1970-09-25|2026-03-20|  53.82|
+------+-----+---------------+----------+-------+
```

<br/>

```
$ docker compose down -v
```


<br/><br/>

---

<br/>

<a href="https://k8s.ru/">Предложить инженеру работу / подработку на проекте с kubernetes, microservices, machine learning, big data, golang</a>
