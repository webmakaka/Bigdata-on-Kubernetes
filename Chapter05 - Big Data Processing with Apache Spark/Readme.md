# Chapter 05 - Big Data Processing with Apache Spark


<br/>

```
$ java --version
openjdk 17.0.18 2026-01-20
OpenJDK Runtime Environment (build 17.0.18+8-Ubuntu-122.04.1)
OpenJDK 64-Bit Server VM (build 17.0.18+8-Ubuntu-122.04.1, mixed mode, sharing)
```

<!-- <br/>

```
$ sudo vi /etc/hosts
127.0.0.1 postgres
``` -->

<br/>

```
$ export PYTHON_VERSION=3.8.12
$ export PROJECT_NAME=big_data
```

<br/>

```
$ pyenv install ${PYTHON_VERSION}
$ pyenv virtualenv ${PYTHON_VERSION} ${PROJECT_NAME}-env
$ source ${PYENV_ROOT}/versions/${PROJECT_NAME}-env/bin/activate
$ mkdir -p  ~/projects/dev/python/${PROJECT_NAME}
$ cd ~/projects/dev/python/${PROJECT_NAME}
```

<br/>

```
$ pip install pyspark
```

<br/>

```
$ spark-submit --version
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.5.8
      /_/
                        
Using Scala version 2.12.18, OpenJDK 64-Bit Server VM, 17.0.18
Branch HEAD
Compiled by user runner on 2026-01-12T04:16:44Z
Revision 5a48a37b2dbd7b51e3640cd1d947438459556cc6
```

<br/>

```
$ git clone git@github.com:webmakaka/Bigdata-on-Kubernetes.git
```

<br/>

```
$ cd Bigdata-on-Kubernetes/Chapter05\ -\ Big\ Data\ Processing\ with\ Apache\ Spark/
```

<br/>

```
$ pip install --upgrade pip
$ pip install jupyterlab requests
```

<br/>

```
$ python get_titanic_data.py
$ python get_imdb_data.py
```

<br/>

```
$ jupyter lab
```

<br/>

```
run -> read_titanic_dataset.ipynb
run -> analyzing_imdb_data.ipynb
```

<br/>

http://localhost:4040/jobs/


<br/><br/>

---

<br/>

<a href="https://k8s.ru/">Предложить инженеру работу / подработку на проекте с kubernetes, microservices, machine learning, big data, golang</a>
