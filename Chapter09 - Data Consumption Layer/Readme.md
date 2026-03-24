# Chapter 09 - Data Consumption Layer

### [FAIL!] Deploying Trino in Kubernetes


```
$ helm repo add bigdata-gradiant https://gradiant.github.io/bigdata-charts/
```

```
// $ helm uninstall hive-metastore -n trino 
$ helm install hive-metastore bigdata-gradiant/hive-metastore -f hms-values.yaml -n trino --create-namespace
```

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
// $ helm uninstall trino -n trino
$ helm install trino trino/trino -f custom_values.yaml -n trino --create-namespace --version 0.19.0
```

<br/>

```
$ kubectl get pods -n trino
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

<br/>

<img src="../img/chapter09-pic01.png">

<img src="../img/chapter09-pic02.png">

<br/>

Download the dataset from https://github.com/neylsoncrepalde/titanic_data_with_semicolon and store the CSV file in an S3 bucket inside a folder named titanic.


```
SQL> select * from hive."bdok-database".titanic
```


```
SQL> select
    pclass,
    sex, COUNT(1) as people_count,
    AVG(age) as avg_age
from hive."bdok-database".titanic
group by pclass, sex
order by sex, pclass
```


<br/>

#### [OK!] Deploying Elasticsearch in Kubernetes

<br/>

https://artifacthub.io/packages/helm/elastic/eck-operator/2.12.1

<br/>

```
// Install elasticsearch operator
$ cd Chapter09
```

<br/>

```
// $ helm repo add elastic https://helm.elastic.co
```

<br/>

```
// Do not works for me, because Russia has been banned
// $ helm install elastic-operator elastic/eck-operator -n elastic --create-namespace --version 2.12.1
```

<br/>

```
$ helm install elastic-operator ./eck-operator-2.12.1/eck-operator -n elastic --create-namespace
```


<br/>

```
$ cd elasticsearch/
$ kubectl apply -f elastic_cluster.yaml -n elastic
$ kubectl apply -f kibana.yaml -n elastic
```

<br/>

```
$ kubectl get pods -n elastic
```

<br/>

```
$ kubectl get elastic -n elastic
```

<br/>

```
$ kubectl get elasticsearch -n elastic
```

<br/>

```
$ kubectl describe elastic -n elastic
```

<br/>

```
$ kubectl get secret elastic-es-elastic-user -n elastic -o go-template='{{.data.elastic | base64decode}}'
```

<br/>

```
$ kubectl get svc -n elastic
```

<br/>

```
// Kibana will not accept regular HTTP protocol connections
// elastic / 
https://192.168.49.20:5601
```

KIBANA 

--> Explore on my own

Data Views

https://192.168.49.20:5601/app/management/kibana/dataViews

Upload a file

https://github.com/neylsoncrepalde/titanic_data_with_semicolon








Dashboards -> Create a dashboard -> Create visualization.



<br/><br/>

---

<br/>

<a href="https://k8s.ru/">Предложить инженеру работу / подработку на проекте с kubernetes, microservices, machine learning, big data, golang</a>
