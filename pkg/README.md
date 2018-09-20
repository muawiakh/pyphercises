# Deploy on Kubernetes(minikube)

## Install minikube

To install minikube, kubectl please follow this [tutorial](https://kubernetes.io/docs/tasks/tools/install-minikube/).

To verify that minikube is running properly:
```bash
$ minikube status
minikube: Running
cluster: Running
kubectl: Correctly Configured: pointing to minikube-vm at <some-IP-address>
```

## Clone pyphercises
```bash
$ git clone https://github.com/muawiakh/pyphercises.git
$ cd pyphercises/
$ git checkout release-workflow
```

## Set minikube context
You can see which context is being used using:

```bash
$ kubectl config get-contexts
<Output has a list of contexts you might have>
$ # The active one is with '*' before it.
$ # Make sure minikube exists there. Otherwise,
$ # make sure minikube and kubectl are installed properly
```

To make minikube the default context:
```bash
$ kubectl config use-context minikube
Switched to context "minikube".
```

## Configure Docker repository
To make sure we are using the Docker repo hosted inside `minikube`
and not Dockerhub, please run:

```bash
eval $(minikube docker-env)
```

To make sure we are using our local repo, verify:

```bash
$ docker images
$ # Long output
$ # If output contains images from `k8s.gcr.io/...`
$ # Then we are good.
```

## Build pyphercises app
Build the pyphercises version app and make sure it is available on
the local Docker repo.

```bash
$ # Make sure you are inside the directory pyphercises cloned github repo
$ # and using the sam terminal where you configure the docker repository
$ # using `eval $(minikube docker-env)`
$ make build-oldest
```

To verify that the image is built and hosted on the local Docker repo:
```bash
$ docker images | grep pyphercises/app
pyphercises/app    v3.0.0    <ID>    <Time of creation>    <Size>
```


## Deploy
To deploy our pyphercises app, we need a Kubernetes service and a deployment.
Replicas for the deployment are controlled and monitored by the ReplicationController inside
Kubernetes and the Service acts as the Loadbalancer/Service discovery endpoint for our service.

```bash
$ # Make sure you are inside the directory pyphercises cloned github repo
$ cd pkg/k8s/
$ # Deploying the service
$ kubectl apply -f versionApp-svc.yaml
service "version-app-svc" created

$ # Verify
$ kubectl get svc
NAME              CLUSTER-IP      EXTERNAL-IP   PORT(S)                 AGE
kubernetes        <clusterIP>       <none>        443/TCP              <age>
version-app-svc   <some IP address> <nodes>       5000:<some port>/TCP <age>

$ # OR
$ minikube service list
|-------------|----------------------|-----------------------------|
|  NAMESPACE  |         NAME         |             URL             |
|-------------|----------------------|-----------------------------|
| default     | kubernetes           | No node port                |
| default     | **version-app-svc    | http://<some IP>:<Port>     |
| kube-system | kube-dns             | No node port                |
| kube-system | kubernetes-dashboard | http://<some IP>:<Port>     |
|-------------|----------------------|-----------------------------|

$ # Our service is named `version-app-svc`

$ # Deploying the app
$ kubectl apply -f versionApp-dep.yaml
deployment "version-app-dep" created

$ # Verify
$ kubectl get pods
NAME                    READY     STATUS    RESTARTS   AGE
version-app-dep-<uuid>   1/1       Running   0          <age>
version-app-dep-<uuid>   1/1       Running   0          <age>
version-app-dep-<uuid>   1/1       Running   0          <age>
$ # If pods are in are Creating state , wait a little

$ # Verify application is up and running
$ # Check the URL provided from the command `minikube service list`
$ # | default     | **version-app-svc    | http://<some IP>:<Port>     |
$ # Open browser or another terminal
$ curl <URL> | jq || curl <URL>
```