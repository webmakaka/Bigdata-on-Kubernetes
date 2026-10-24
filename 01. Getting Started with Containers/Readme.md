# Chapter 01 - Getting Started with Containers

<br/>

### Batch processing job

```
$ docker build -f Dockerfile_job -t data_processing_job:1.0 .
$ docker run --name data_processing data_processing_job:1.0
```

<br/>

### API service

```
$ docker build -t my_api:1.0 .
$ docker run -p 8087:8087 -d --rm --name api my_api:1.0
```


```
http://localhost:8087/joke
```

<br/><br/>

---

<br/>

<a href="https://k8s.ru/">Предложить инженеру работу / подработку на проекте с kubernetes, microservices, machine learning, big data, golang</a>
