# Chapter 10 - Building a Big Data Pipeline on Kubernetes

### Checking the deployed tools

* Minio
* Hive Metastore
* Trino
* Ariflow

<br/>

```
$ kubectl get pods -n trino
NAME                                 READY   STATUS    RESTARTS   AGE
trino-coordinator-57cc8c466f-7wchh   1/1     Running   0          16m
trino-worker-9b6b9f57-7p7gx          1/1     Running   0          16m
trino-worker-9b6b9f57-bw8nh          1/1     Running   0          16m
```

<br/>

```
$ helm install airflow apache-airflow/airflow --namespace airflow --create-namespace -f custom_values.yaml
```
