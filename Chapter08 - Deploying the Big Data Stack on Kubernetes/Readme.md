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

```
$ {
    minikube --profile ${PROFILE} config set memory ${MEMORY}
    minikube --profile ${PROFILE} config set cpus ${CPUS}
    minikube --profile ${PROFILE} config set disk-size ${HDD}

    minikube --profile ${PROFILE} config set driver ${DRIVER}

    minikube --profile ${PROFILE} config set kubernetes-version ${KUBERNETES_VERSION}
    minikube start --profile ${PROFILE} --embed-certs

    // Enable ingress
    minikube addons --profile ${PROFILE} enable ingress

    // Enable registry
    // minikube addons --profile ${PROFILE} enable registry

    // Enable metallb
    minikube addons --profile ${PROFILE} enable metallb
}
```

<br/>

### [Нужен addon Metal LB](//docs.k8s.ru/tools/containers/kubernetes/utils/metal-lb/minikube/setup/addon/)

<br/>

### [Нужно добавить MINIO для S3](//docs.gitops.ru/tools/containers/kubernetes/utils/minio/)



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

<br/>

```
$ kubectl create secret generic aws-credentials --from-literal=aws_access_key_id=admin --from-literal=aws_secret_access_key="password123" -n spark-operator
```


Создаю bucket spark и загружаю в него файл spark_job.py, предварительно заменив переменные <YOUR_BUCKET> <YOUR_NEW_BUCKET>


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

### [OK!] Deploying Kafka on Kubernetes


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
// Нужно ждать!
$ kubectl get pods -n kafka
NAME                                        READY   STATUS    RESTARTS   AGE
kafka-cluster-kafka-0                       1/1     Running   0          63s
kafka-cluster-kafka-1                       1/1     Running   0          63s
kafka-cluster-kafka-2                       1/1     Running   0          63s
kafka-cluster-zookeeper-0                   1/1     Running   0          87s
kafka-cluster-zookeeper-1                   1/1     Running   0          87s
kafka-cluster-zookeeper-2                   1/1     Running   0          87s
strimzi-cluster-operator-6f9fbb4c75-zxhh8   1/1     Running   0          13m
```

```
$ kubectl get svc -n kafka
NAME                                     TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)                                        AGE
kafka-cluster-kafka-0                    LoadBalancer   10.110.8.234     192.168.49.21   9094:31956/TCP                                 2m19s
kafka-cluster-kafka-1                    LoadBalancer   10.111.210.63    192.168.49.22   9094:32576/TCP                                 2m19s
kafka-cluster-kafka-2                    LoadBalancer   10.104.36.248    192.168.49.23   9094:32678/TCP                                 2m19s
kafka-cluster-kafka-bootstrap            ClusterIP      10.108.187.242   <none>          9091/TCP,9092/TCP,9093/TCP                     2m19s
kafka-cluster-kafka-brokers              ClusterIP      None             <none>          9090/TCP,9091/TCP,8443/TCP,9092/TCP,9093/TCP   2m19s
kafka-cluster-kafka-external-bootstrap   LoadBalancer   10.109.196.85    192.168.49.20   9094:30646/TCP                                 2m19s
kafka-cluster-zookeeper-client           ClusterIP      10.110.241.105   <none>          2181/TCP                                       2m43s
kafka-cluster-zookeeper-nodes            ClusterIP      None             <none>          2181/TCP,2888/TCP,3888/TCP                     2m43s
```


<br/>

```
$ minikube --profile ${PROFILE} stop && minikube --profile ${PROFILE} delete
```


<br/><br/>

---

<br/>

<a href="https://k8s.ru/">Предложить инженеру работу / подработку на проекте с kubernetes, microservices, machine learning, big data, golang</a>
