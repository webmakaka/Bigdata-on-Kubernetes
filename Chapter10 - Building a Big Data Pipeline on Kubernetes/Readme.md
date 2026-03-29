# Chapter 10 - Building a Big Data Pipeline on Kubernetes

### Checking the deployed tools

<br/>

* Minio
* Hive Metastore
* Trino
* AirFlow
* Spark

<br/>

**Mini**

```
Crete bucket: imdb-datasets, airflow-logs
```

<br/>

**Trino**

```
$ kubectl get pods -n trino
NAME                                 READY   STATUS    RESTARTS   AGE
trino-coordinator-57cc8c466f-7wchh   1/1     Running   0          16m
trino-worker-9b6b9f57-7p7gx          1/1     Running   0          16m
trino-worker-9b6b9f57-bw8nh          1/1     Running   0          16m
```

<br/>

**AirFlow**

```
gitSync:
***
    repo: https://github.com/webmakaka/Bigdata-on-Kubernetes.git
***
    subPath: "Chapter10 - Building a Big Data Pipeline on Kubernetes/batch/dags"
***
```

<br/>

```
// Roles
$ kubectl apply -f ./airflow_deployment/rolebinding_for_airflow.yaml
```

<br/>

```bash
// $ helm install airflow apache-airflow/airflow --namespace airflow --create-namespace -f airflow_deployment/custom_values.yaml --version 1.13.1
```

<br/>

```bash
// $ helm uninstall airflow --namespace airflow
$ helm install airflow --namespace airflow --create-namespace -f airflow_deployment/custom_values.yaml ../../kubernetes-data-platform/helm-charts/airflow/
```

<br/>

```
$ kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow
```

<br/>

```
// OK!
// admin / admin
http://localhost:8080/
```


<br/><br/>

---

<br/>

<a href="https://k8s.ru/">Предложить инженеру работу / подработку на проекте с kubernetes, microservices, machine learning, big data, golang</a>
