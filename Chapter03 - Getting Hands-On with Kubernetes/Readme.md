# Chapter 03 - Getting Hands-On with Kubernetes

<br/>

### Deploying a local cluster using Kind

```
$ kind create cluster
```

```
$ kubectl cluster-info
```

<br/>

### Running your API on Kubernetes

```
$ docker login
```

```
$ docker build -t webmakaka/jokeapi:v1 .
$ docker push webmakaka/jokeapi:v1
```

<br/>

### Creating the deployment

```
$ kubectl create namespace jokeapi
```

<br/>

```yaml
$ cat << EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jokeapi
  namespace: jokeapi
spec:
  replicas: 2
  selector:
    matchLabels:
      app: jokeapi 
  template:
    metadata:
      labels:
        app: jokeapi
    spec:
      containers:
      - name: jokeapi
        image: neylsoncrepalde/jokeapi:v1
        imagePullPolicy: Always
        ports:
        - containerPort: 8087 
EOF
```

<br/>

```
$ kubectl get deployments -n jokeapi
NAME      READY   UP-TO-DATE   AVAILABLE   AGE
jokeapi   2/2     2            2           12s
```

<br/>

```
$ kubectl get pods -n jokeapi
NAME                      READY   STATUS    RESTARTS   AGE
jokeapi-8d7df9b57-cv72p   1/1     Running   0          33s
jokeapi-8d7df9b57-glfwk   1/1     Running   0          33s
```

<br/>

```yaml
$ cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: jokeapi
  namespace: jokeapi
spec:
  selector:
    app: jokeapi
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8087
EOF
```

<br/>

```
$ kubectl get services -n jokeapi
NAME      TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
jokeapi   ClusterIP   10.96.97.200   <none>        80/TCP    22s
```

<br/>

```
$ kubectl port-forward svc/jokeapi 8080:80 -n jokeapi
```

<br/>

```
// OK!
http://localhost:8080/joke
```

<br/>

### Running a data processing job in Kubernetes

```
$ docker build --platform linux/amd64 -f Dockerfile_job -t webmakaka/dataprocessingjob:v1 .
$ docker push webmakaka/dataprocessingjob:v1
```

```
$ kubectl create namespace datajob
```

<br/>

```yaml
$ cat << EOF | kubectl apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: dataprocessingjob
  namespace: datajob
spec:
  template:
    spec:
      containers:
      - name: dataprocessingjob
        image: neylsoncrepalde/dataprocessingjob:v1
      restartPolicy: Never
  backoffLimit: 4
EOF
```

<br/>

```
$ kubectl get jobs -n datajob
NAME                STATUS     COMPLETIONS   DURATION   AGE
dataprocessingjob   Complete   1/1           3s         4s
```

<br/>

```
$ kubectl get pods -n datajob
```

<br/>

```
$ kubectl logs dataprocessingjob-klmwq -n datajob
Index([0, 1, 2, 3, 4, 5, 6, 7, 8, 'newcolumn'], dtype='object')
   0    1   2   3    4     5      6   7  8  newcolumn
0  6  148  72  35    0  33.6  0.627  50  1       67.2
1  1   85  66  29    0  26.6  0.351  31  0       53.2
2  8  183  64   0    0  23.3  0.672  32  1       46.6
3  1   89  66  23   94  28.1  0.167  21  0       56.2
4  0  137  40  35  168  43.1  2.288  33  1       86.2
(768, 10)
```

<br/><br/>

---

<br/>

<a href="https://k8s.ru/">Предложить инженеру работу / подработку на проекте с kubernetes, microservices, machine learning, big data, golang</a>
