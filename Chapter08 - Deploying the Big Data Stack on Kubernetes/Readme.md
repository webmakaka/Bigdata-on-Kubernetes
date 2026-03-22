# Chapter 08 - Deploying the Big Data Stack on Kubernetes

<br/>

```
// Версия старше требует новую версию strimzi-cluster-operator, где уже нет zookeeper
$ export \
    PROFILE=${USER}-minikube \
    CPUS=4 \
    MEMORY=8G \
    HDD=20G \
    DRIVER=docker \
    KUBERNETES_VERSION=v1.31.0
```

<br/>

### [FAIL!] Deploying Spark on Kubernetes

<br/>

```
$ helm install spark-operator https://github.com/kubeflow/spark-operator/releases/download/spark-operator-chart-1.1.27/spark-operator-1.1.27.tgz \
  --namespace spark-operator \
  --create-namespace \
  --set webhook.enable=true
```

<br/>

```
$ kubectl get pods -n spark-operator
NAME                                READY   STATUS      RESTARTS   AGE
spark-operator-6f5b9cf5f7-mppxm     1/1     Running     0          76s
spark-operator-webhook-init-mbkwg   0/1     Completed   0          2m1s
```

<br/>

```
$ cd /home/marley/projects/dev/python/big_data/Bigdata-on-Kubernetes/Chapter08/spark
```

```
$ kubectl apply -f spark_job.yaml -n spark-operator
```

```
$ kubectl get sparkapplication -n spark-operator
```

```
$ kubectl get sparkapplication -n spark-operator
```

```
$ kubectl describe sparkapplication/test-spark-job -n spark-operator
```

```
$ kubectl logs test-spark-job-driver -n spark-operator
```

```
$ kubectl delete sparkapplication/test-spark-job -n spark-operator
```

<br/>

### [FAIL!] Deploying Airflow on Kubernetes (не заработал)

```
$ helm repo add apache-airflow https://airflow.apache.org
```

<br/>

```
$ cd /home/marley/projects/dev/python/big_data/Bigdata-on-Kubernetes/Chapter08/airflow
```

<br/>

```
$ vi custom_values.yaml
```

<br/>

```
$ helm install airflow apache-airflow/airflow --namespace airflow --create-namespace -f custom_values.yaml
```

<br/>

Ошибка!

<br/>

```
$ kubectl get svc -n airflow
```


<br/>

### [FAIL!] Deploying Kafka on Kubernetes


https://artifacthub.io/packages/helm/strimzi/strimzi-kafka-operator


```
$ helm repo add strimzi https://strimzi.io/charts/
```

<br/>

```
// $ helm delete kafka -n kafka
$ helm install kafka strimzi/strimzi-kafka-operator --namespace kafka --create-namespace --version 0.44.0
```

<br/>

```
$ helm status kafka -n kafka
```

<br/>

```
$ watch -n 2 -c 'kubectl get pods -n kafka'
NAME                                        READY   STATUS    RESTARTS   AGE
strimzi-cluster-operator-7d9bbbdf5d-hxhxf   1/1     Running   0          108s
```

```
$ cd Bigdata-on-Kubernetes/Chapter08/kafka
```

```
// deploy the cluster to Kubernetes
$ kubectl apply -f kafka_jbod.yaml -n kafka
```

```
$ kubectl get kafka -n kafka
NAME            DESIRED KAFKA REPLICAS   DESIRED ZK REPLICAS   READY   METADATA STATE   WARNINGS
kafka-cluster   3                        3                          
```

<br/>

```
$ kubectl get pods -n kafka
NAME                                        READY   STATUS    RESTARTS   AGE
kafka-cluster-zookeeper-0                   1/1     Running   0          102s
kafka-cluster-zookeeper-1                   1/1     Running   0          101s
kafka-cluster-zookeeper-2                   1/1     Running   0          101s
strimzi-cluster-operator-6f9fbb4c75-zxhh8   1/1     Running   0          3m3s
```


<br/>

```
$ kind delete cluster
```


<br/><br/>

---

<br/>

<a href="https://k8s.ru/">Предложить инженеру работу / подработку на проекте с kubernetes, microservices, machine learning, big data, golang</a>
