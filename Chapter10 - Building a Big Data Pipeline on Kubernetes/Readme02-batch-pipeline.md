# Chapter 10 - Building a Big Data Pipeline on Kubernetes - Building a real-time pipeline

### Checking the deployed tools

<br/>

* Minio
* AirFlow
* Spark
* Kafka
* Elastic


<br/>

**postgres**

```
~$ kubectl port-forward pod/postgres 5432:5432
```

<br/>

```
$ export PROJECT_NAME=big_data
$ source ${PYENV_ROOT}/versions/${PROJECT_NAME}-env/bin/activate
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


```
$ cd streaming/elastic_deployment
$ kubectl apply -f elastic_cluster.yaml -n kafka
$ kubectl apply -f kibana.yaml -n kafka
```

<br/>


```bash
$ kubectl get secret elastic-es-elastic-user -n kafka -o go-template='{{.data.elastic | base64decode}}'
```

<br/>

We must configure certificates
and keys that will allow Kafka Connect to correctly connect to Elastic.

<br/>

```bash
$ kubectl get secret elastic-es-http-certs-public -n kafka --output=go-template='{{index .data "ca.crt" | base64decode}}' > ca.crt

$ kubectl get secret elastic-es-http-certs-public -n kafka --output=go-template='{{index .data "tls.crt" | base64decode}}' > tls.crt

$ kubectl get secret elastic-es-http-certs-internal -n kafka --output=go-template='{{index .data "tls.key" | base64decode}}' > tls.key
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

connect_cluster.yaml

<br/>

```
$ kubectl get svc -n kafka
```

<br/>

```
$ kubectl get secret -n kafka
```

<br/>

```
$ kubectl apply -f connect_cluster.yaml -n kafka
```

<br/>


```
$ kubectl apply -f connectors/jdbc_source.yaml -n kafka
```

<br/>

```
$ kubectl get kafkaconnector -n kafka
$ kubectl describe kafkaconnector jdbc-source -n kafka
```

<br/>

```
$ kubectl exec kafka-cluster-kafka-0 -n kafka -c kafka -it -- bin/
$ kafka-console-consumer.sh --bootstrap-server localhost:9092
--from-beginning --topic src-customers
```

<br/>

### Real-time processing with Spark


<br/>

```bash
$ kubectl create serviceaccount spark -n kafka
$ kubectl create clusterrolebinding spark-role-kafka --clusterrole=edit --serviceaccount=kafka:spark -n kafka
```


<br/>

```bash
$ kubectl get secrets -n kafka
```



<br/>

```bash
$ kubectl create secret generic aws-credentials --from-literal=aws_access_key_id=<YOUR_ACCESS_KEY_ID> --from-literal=aws_secret_access_key="<YOUR_SECRET_ACCESS_KEY>" -n
kafka
```

<br/>

```bash
$ kubectl apply -f spark_streaming_job.yaml -n kafka
```

<br/>

```bash
$ kubectl describe sparkapplication spark-streaming-job -n kafka
$ kubectl get pods -n kafka
```

<br/>

```bash
$ kubectl exec kafka-cluster-kafka-0 -n kafka -c kafka -it -- bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic customers-transformed
```

<br/>

### Deploying the Elasticsearch sink connector


<br/>

```
$ kubectl apply -f connectors/es_sink.yaml -n kafka
```

<br/>

```
$ kubectl describe kafkaconnector es-sink -n kafka
```

<br/>

```
$ kubectl get svc -n kafka
```

<br/><br/>

---

<br/>

<a href="https://k8s.ru/">Предложить инженеру работу / подработку на проекте с kubernetes, microservices, machine learning, big data, golang</a>
