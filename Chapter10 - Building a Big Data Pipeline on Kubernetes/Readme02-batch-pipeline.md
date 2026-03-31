# Chapter 10 - Building a Big Data Pipeline on Kubernetes - Building a real-time pipeline

Нужен kubernetes v1.31.0 или разбираться с kafka, старая версия которого не запускается, а новая уже без zookeeper.

### Checking the deployed tools

<br/>

* Minio
* AirFlow
* Spark
* Kafka
* Elastic

<br/>

Minio -> создаем bucket "spark-jobs" и загружаем в него файл streaming/spark_processing/spark_streaming_job.py и bucket "spark-checkpoint"

<br/>

**postgres**

```
$ kubectl port-forward svc/postgres-postgresql -n postgres 5432:5432
```

<br/>

```
$ cd Chapter07/connect/
$ pip install -r ./simulations/requirements.txt
```

<br/>

```bash
$ cd Chapter10
$ cd streaming/

// to populate our database with some data
$ python simulations.py --host localhost -p postgres

// Завершить спустя какое-то количество
$ ^C
```

<br/>

### Deploying Kafka Connect and Elasticsearch

**kafka**

https://artifacthub.io/packages/helm/strimzi/strimzi-kafka-operator

```
$ helm repo add strimzi https://strimzi.io/charts/
```

<br/>

```
// $ helm delete kafka -n kafka
$ helm install kafka strimzi/strimzi-kafka-operator \
    --namespace kafka --create-namespace \
    --version 0.44.0
```

<br/>

```
$ cd Bigdata-on-Kubernetes/Chapter08/kafka
$ kubectl apply -f kafka_jbod.yaml -n kafka
```

<br/>


**Elasticsearch**

```
$ cd streaming/
$ kubectl apply -f elastic_deployment/elastic_cluster.yaml -n elastic
$ kubectl apply -f elastic_deployment/kibana.yaml -n elastic
```

<br/>


```bash
$ kubectl get secret elastic-es-elastic-user -n elastic -o go-template='{{.data.elastic | base64decode}}'
```

<br/>

We must configure certificates and keys that will allow Kafka Connect to correctly connect to Elastic.

<br/>

```bash
$ kubectl get secret elastic-es-http-certs-public -n elastic --output=go-template='{{index .data "ca.crt" | base64decode}}' > ca.crt

$ kubectl get secret elastic-es-http-certs-public -n elastic --output=go-template='{{index .data "tls.crt" | base64decode}}' > tls.crt

$ kubectl get secret elastic-es-http-certs-internal -n elastic --output=go-template='{{index .data "tls.key" | base64decode}}' > tls.key
```

<br/>

```
$ sudo apt update
$ sudo apt install openjdk-21-jre-headless -y
```

<br/>

```bash
$ openssl pkcs12 -export -in tls.crt -inkey tls.key -CAfile ca.crt -caname root -out keystore.p12 -password pass:BCoqZy82BhIhHv3C -name es-keystore

$ keytool -importkeystore -srckeystore keystore.p12 -srcstoretype PKCS12 -srcstorepass BCoqZy82BhIhHv3C -deststorepass OfwxynZ8KATfZSZe -destkeypass OfwxynZ8KATfZSZe -destkeystore keystore.jks -alias es-keystore
```

<br/>

```
$ kubectl create secret generic es-keystore --from-file=keystore.jks -n kafka
```

<br/>

**Kafka**

Этот манифест разворачивает Kafka Connect — специальный сервис-прослойку, который умеет автоматически перекачивать данные между Kafka и внешними системами (S3, Postgres, Elasticsearch).

```
$ kubectl apply -f connect_cluster.yaml -n kafka
```

<br/>

```
$ kubectl create secret generic aws-credentials \
  --from-literal=aws_access_key_id='admin' \
  --from-literal=aws_secret_access_key='password' \
  -n kafka
```

<br/>

```
$ kubectl get pods -n kafka
NAME                                        READY   STATUS    RESTARTS   AGE
kafka-cluster-kafka-0                       1/1     Running   0          15m
kafka-cluster-zookeeper-0                   1/1     Running   0          16m
kafka-connect-cluster-connect-0             1/1     Running   0          80s
strimzi-cluster-operator-6f9fbb4c75-tg7pr   1/1     Running   0          23m
```

<br/>

Следующий манифест создает сам Connector — конкретную задачу для Kafka Connect. Он будет «выкачивать» данные из таблицы public.customers в PostgreSQL и записывать их в Kafka.

<br/>

```
$ kubectl apply -f connectors/jdbc_source.yaml -n kafka
```

<br/>

```
$ kubectl get kctr jdbc-source -n kafka -o yaml
```

<br/>

```
// OK!
$ kubectl exec -it postgres-postgresql-0 -n postgres -- psql -U postgres -d postgres -c "UPDATE customers SET dt_update = NOW();"
```

<br/>

```
// Check messages in the topic
// Ok!
$ kubectl exec kafka-cluster-kafka-0 -n kafka -c kafka -it -- bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic src-customers
```

<br/>

### Real-time processing with Spark

<br/>

https://github.com/webmakaka/kubernetes-data-platform/tree/main/05.1.spark

<br/>

```bash
$ kubectl create secret generic aws-credentials \
  --from-literal=aws_access_key_id='admin' \
  --from-literal=aws_secret_access_key='password' \
  -n spark-operator
```

<br/>

```yaml
$ cat << 'EOF' | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: spark
  namespace: spark-operator
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: spark-role
  namespace: spark-operator
rules:
  - apiGroups: [""]
    resources: ["pods", "services", "configmaps", "secrets"]
    verbs: ["*"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: spark-role-binding
  namespace: spark-operator
subjects:
  - kind: ServiceAccount
    name: spark
    namespace: spark-operator
roleRef:
  kind: Role
  name: spark-role
  apiGroup: rbac.authorization.k8s.io
EOF
```

<br/>

```
// Creating a service account for spark
$ kubectl create serviceaccount spark -n kafka
$ kubectl create clusterrolebinding spark-role-kafka --clusterrole=edit --serviceaccount=kafka:spark -n kafka
```

<br/>

```
// Deploy spark streaming job
$ kubectl apply -f spark_streaming_job.yaml -n kafka
$ kubectl describe sparkapplication spark-streaming-job -n kafka
```

<br/>

```
$ kubectl get pods -n kafka
NAME                                        READY   STATUS              RESTARTS   AGE
kafka-cluster-kafka-0                       1/1     Running             0          47m
kafka-cluster-zookeeper-0                   1/1     Running             0          48m
kafka-connect-cluster-connect-0             1/1     Running             0          33m
spark-streaming-job-driver                  0/1     ContainerCreating   0          12s
strimzi-cluster-operator-6f9fbb4c75-tg7pr   1/1     Running             0          55m
```

<br/>

```
// Check messages in the transformed topic
// Ok!
$ kubectl exec kafka-cluster-kafka-0 -n kafka -c kafka -it -- bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic customers-transformed
```

<br/>

```
$ kubectl get pods -n kafka
NAME                                        READY   STATUS    RESTARTS   AGE
consumefromkafka-22facd9d418c3ab9-exec-1    1/1     Running   0          3m38s
kafka-cluster-kafka-0                       1/1     Running   0          93m
kafka-cluster-zookeeper-0                   1/1     Running   0          93m
kafka-connect-cluster-connect-0             1/1     Running   0          78m
spark-streaming-job-driver                  1/1     Running   0          3m57s
strimzi-cluster-operator-6f9fbb4c75-tg7pr   1/1     Running   0          101m
```


<br/>

### Deploying the Elasticsearch sink connector

<br/>

```
// Deploy elasticsearch sink connector
$ kubectl apply -f connectors/es_sink.yaml -n kafka
```

<br/>

```
$ kubectl get kctr es-sink -n kafka -o yaml
```

<br/>

```
// Check the es sink connector
$ kubectl describe kafkaconnector es-sink -n kafka

Message:               PUT /connectors/es-sink/config returned 400 (Bad Request): Connector configuration is invalid and contains the following 1 error(s):
Failed to create client to verify connection. Failed to load SSL keystore /opt/kafka/external-configuration/es-keystore-volume/keystore.jks of type JKS
You can also find the above list of errors at the endpoint `/connector-plugins/{connectorType}/config/validate`
```

<br/>

```
$ kubectl edit kafkaconnect kafka-connect-cluster -n kafka
```

<br/>

```
  externalConfiguration:
    env:
    - name: AWS_ACCESS_KEY_ID
      valueFrom:
        secretKeyRef:
          key: aws_access_key_id
          name: aws-credentials
    - name: AWS_SECRET_ACCESS_KEY
      valueFrom:
        secretKeyRef:
          key: aws_secret_access_key
          name: aws-credentials
    volumes:
      - name: es-keystore-volume     
        secret:
          secretName: es-keystore
```

<br/>

```
# Находим имя пода
$ POD_NAME=$(kubectl get pods -n kafka -l strimzi.io/kind=KafkaConnect -o name)

# Проверяем содержимое папки
$ kubectl exec -it $POD_NAME -n kafka -- ls -lR /opt/kafka/external-configuration/es-keystore-volume/
```

<br/>

```
/opt/kafka/external-configuration/es-keystore-volume/:
total 0
lrwxrwxrwx 1 root root 19 Mar 31 02:19 keystore.jks -> ..data/keystore.jks
```


<br/>

```
$ kubectl delete secret es-keystore -n kafka
$ kubectl create secret generic es-keystore --from-file=keystore.jks -n kafka```

$ kubectl delete kctr es-sink -n kafka
$ kubectl apply -f es_sink.yaml -n kafka
```

<br/>

```
Message:               PUT /connectors/es-sink/config returned 400 (Bad Request): Connector configuration is invalid and contains the following 4 error(s):
Could not connect to Elasticsearch. Error message: method [HEAD], host [https://elastic-es-http.elastic:9200], URI [/], status line [HTTP/1.1 401 Unauthorized]
Could not authenticate the user. Check the 'connection.username' and 'connection.password'. Error message: method [HEAD], host [https://elastic-es-http.elastic:9200], URI [/], status line [HTTP/1.1 401 Unauthorized]
Could not authenticate the user. Check the 'connection.username' and 'connection.password'. Error message: method [HEAD], host [https://elastic-es-http.elastic:9200], URI [/], status line [HTTP/1.1 401 Unauthorized]
Could not connect to Elasticsearch. Check your SSL settings.Error message: method [HEAD], host [https://elastic-es-http.elastic:9200], URI [/], status line [HTTP/1.1 401 Unauthorized]
```

<br/>

```
$ kubectl get secret elastic-es-elastic-user -n elastic -o jsonpath="{.data.elastic}" | base64 --decode; echo
X4Xb63q7352m9fu8LoFDAyM2
```

<br/>

```
$ vi es_sink.yaml

***
connection.password: X4Xb63q7352m9fu8LoFDAyM2
***
```

<br/>

```
$ kubectl apply -f es_sink.yaml -n kafka
```

<br/>

```
$ kubectl describe kafkaconnector es-sink -n kafka
Name:         es-sink
Namespace:    kafka
Labels:       strimzi.io/cluster=kafka-connect-cluster
Annotations:  <none>
API Version:  kafka.strimzi.io/v1beta2
Kind:         KafkaConnector
Metadata:
  Creation Timestamp:  2026-03-31T02:34:47Z
  Generation:          2
  Resource Version:    20145
  UID:                 bd434ee4-9865-42a2-bb8b-8aad32522d66
Spec:
  Class:  io.confluent.connect.elasticsearch.ElasticsearchSinkConnector
  Config:
    batch.size:                             1
    connection.password:                    X4Xb63q7352m9fu8LoFDAyM2
    connection.url:                         https://elastic-es-http.elastic:9200
    connection.username:                    elastic
    elastic.https.ssl.key.password:         OfwxynZ8KATfZSZe
    elastic.https.ssl.keystore.location:    /opt/kafka/external-configuration/es-keystore-volume/keystore.jks
    elastic.https.ssl.keystore.password:    OfwxynZ8KATfZSZe
    elastic.https.ssl.keystore.type:        JKS
    elastic.https.ssl.truststore.location:  /opt/kafka/external-configuration/es-keystore-volume/keystore.jks
    elastic.https.ssl.truststore.password:  OfwxynZ8KATfZSZe
    elastic.https.ssl.truststore.type:      JKS
    elastic.security.protocol:              SSL
    key.ignore:                             true
    Topics:                                 customers-transformed
  Tasks Max:                                1
Status:
  Conditions:
    Last Transition Time:  2026-03-31T02:41:19.540845996Z
    Status:                True
    Type:                  Ready
  Connector Status:
    Connector:
      State:      RUNNING
      worker_id:  kafka-connect-cluster-connect-0.kafka-connect-cluster-connect.kafka.svc:8083
    Name:         es-sink
    Tasks:
      Id:               0
      State:            RUNNING
      worker_id:        kafka-connect-cluster-connect-0.kafka-connect-cluster-connect.kafka.svc:8083
    Type:               sink
  Observed Generation:  2
  Tasks Max:            1
  Topics:
    customers-transformed
Events:  <none>

```

<br/><br/>

---

<br/>

<a href="https://k8s.ru/">Предложить инженеру работу / подработку на проекте с kubernetes, microservices, machine learning, big data, golang</a>
