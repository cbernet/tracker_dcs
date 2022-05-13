# FastApi Hello 

Test fastapi package to experiment with Kubernetes.

Features: 

- full deployment with helm
- file config maps 
- external secrets
- ingress with alb controller 


## Developer instructions

**Please read this before doing anything**

* [Cynapps documentation](https://github.com/cynapps/documentation/blob/main/README.md) 

Installation: 

```
conda create -n hello python=3.9
conda activate hello
pip install --upgrade pip
pip install -r requirements/local.txt
pip install -e .  
```

## Environment variables 

These secrets will be printed out by the server. 
They are not used for authentication, so set them to whatever you want. 

* `APP_USER`: app user
* `APP_PASSWORD`: app password

Other environment variables:

* `APP_CONFIG`: config yaml file, see [config/foobar.yaml](config/foobar.yaml)

## Running 

```
python hello/app.py
```

Visit the API docs page to try the endpoints:
[http://localhost:5000/docs](http://localhost:5000/docs)

The root endpoint will print: 

* the secrets you have set 
* the rest of your configuration (non-secret config) 


## Running with docker 

Set the secret environment variables. 

Build the docker image: 

```
docker build . -t hello
```

Run: 

```shell
docker run \
 -v $PWD/config:/etc/config \
 -e APP_CONFIG=/etc/config/helloworld.yaml \
 -e APP_USER="john difool" \
 -e APP_PASSWORD=BlackIncal \
 -p 8001:8000 \
 hello \
 uvicorn hello.app:app --host 0.0.0.0
```

Note that: 

* we could first set the secrets `APP_USER` and `APP_PASSWORD`
and pass them implicitly to avoid showing them on the command line 
so that they are not shown on the command line.
* we map the config directory on the host to `/etc/config` in
the container
* the config file is picked up from this directory

Now test : 

```
curl localhost:8001 | json_pp
```

## Deploy on kubernetes

First install your secrets in the Parameter Store using terraform.

Then: 

```
helm install -n hello hello helm/hello
```




