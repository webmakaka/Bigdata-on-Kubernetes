# Chapter 10 - Building a Big Data Pipeline on Kubernetes

### Checking the deployed tools

* Minio
* Hive Metastore
* Trino
* AirFlow

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
    subPath: "Chapter10%20-%20Building%20a%20Big%20Data%20Pipeline%20on%20Kubernetes/batch/dags"
***
```

```
$ kubectl apply -f ./airflow_deployment/rolebinding_for_airflow.yaml 
```

```
$ helm install airflow apache-airflow/airflow --namespace airflow --create-namespace -f airflow_deployment/custom_values.yaml
```
