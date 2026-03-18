# Chapter 06 - Building Pipelines with Apache Airflow

Install the Astro CLI

https://docs.astronomer.io/astro/cli/install-cli

<br/>

```
$ curl -sSL install.astronomer.io | sudo bash -s
```

<br/>

```
$ mkdir ~/tmp/airflow
$ cp -r ./dags ~/tmp/airflow/

$ cd ~/tmp/airflow

$ astro dev init
$ astro dev start
```

<br/>

```
// admin / admin
http://localhost:8080
```

<br/>

```
$ astro dev kill
```


<br/>

### Airflow integration with other tools

Имеет 2 DAG

1. Демо
2. Записывает данные в базу postgres и в облако AWS (если у вас есть такая возможность)

<br/>

При старте ошибка DAG, нужно Airflow -> Admin -> Variables. Добавить переменные см. по коду какие нужны.

<br/>

При старте airflow поднимается база postgres, к которой можно подключиться

// postgres / postgres
// localhost

<br/>

Airflow -> Admin -> Connections

<br/>

```
$ astro dev kill
```

<br/><br/>

---

<br/>

<a href="https://k8s.ru/">Предложить инженеру работу / подработку на проекте с kubernetes, microservices, machine learning, big data, golang</a>
