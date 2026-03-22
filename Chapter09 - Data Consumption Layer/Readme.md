# Chapter 09 - Data Consumption Layer

### Deploying Trino in Kubernetes

<br/>

```
$ helm repo add trino https://trinodb.github.io/charts
```

<br/>

```
$ cd Bigdata-on-Kubernetes/Chapter09/trino
```

<br/>

```
$ helm install trino trino/trino -f custom_values.yaml -n trino --create-namespace --version 0.19.0
```

<br/>

```
$ kubectl get pods -n trino
NAME                                READY   STATUS    RESTARTS   AGE
trino-coordinator-5864b8497-xvb4h   1/1     Running   0          3m36s
trino-worker-6dcf5978d5-dcwjc       1/1     Running   0          3m36s
trino-worker-6dcf5978d5-zl87k       1/1     Running   0          3m36s
```

<br/>

```
$ kubectl get svc -n trino
NAME    TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)          AGE
trino   LoadBalancer   10.109.226.94   192.168.49.20   8080:31473/TCP   13m
```

<br/>

```
// trino
192.168.49.20:8080
```

Dbeaver создать новое соединение с типом trino, скачать драйвера и подключиться.

У меня крашится при попытке посмотреть структуру таблиц в minikube и kind.

<br/>

#### Deploying Elasticsearch in Kubernetes

<br/>

```
$ helm repo add elastic https://helm.elastic.co
```

<br/>

```
$ helm install elastic-operator elastic/eck-operator -n elastic --create-namespace --version 2.12.1
```

<br/>

```
$ /home/marley/projects/dev/python/big_data/Bigdata-on-Kubernetes/Chapter09/elasticsearch
```

<br/>

```
$ kubectl apply -f elastic_cluster.yaml -n elastic
$ kubectl apply -f kibana.yaml -n elastic
```

<br/>

```
$ kubectl get pods -n elastic
```

<br/>

```
$ kubectl get secret elastic-es-elastic-user -n elastic -o go-template='{{.data.elastic | base64decode}}'
```

<br/>

```
$ kubectl get svc -n elastic
```


<br/><br/>

---

<br/>

<a href="https://k8s.ru/">Предложить инженеру работу / подработку на проекте с kubernetes, microservices, machine learning, big data, golang</a>
