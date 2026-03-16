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

### Using an ingress to access the API

<br/>

```
$ kubectl create namespace ingress-nginx
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.3/deploy/static/provider/baremetal/deploy.yaml -n ingress-nginx
```

<br/>

```
$ kubectl edit service ingress-nginx-controller -n ingress-nginx
```

Search for the spec.type field and change its value to LoadBalancer.

<br/>

```yaml
$ cat << EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: jokeapi-ingress
  namespace: jokeapi
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: jokeapi
            port:
              number: 80
EOF
```

<br/>

```
$ kubectl get ingress -n jokeapi
NAME              CLASS   HOSTS   ADDRESS   PORTS   AGE
jokeapi-ingress   nginx   *                 80      37s
```

<br/><br/>

---

<br/>

<a href="https://k8s.ru/">Предложить инженеру работу / подработку на проекте с kubernetes, microservices, machine learning, big data, golang</a>
