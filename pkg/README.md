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

### Scenario: HA and fault tolerance

By default our application has 3 replicas, as specified in the 
`versionApp-dep.yaml` file.

```yaml
replicas: 3
```

The replicas provide HA and the replication controller provides
fault tolerance. To test:

```bash
$ kubectl get pods
NAME                    READY     STATUS    RESTARTS   AGE
version-app-dep-<uuid>   1/1       Running   0          <age>
version-app-dep-<uuid>   1/1       Running   0          <age>
version-app-dep-<uuid>   1/1       Running   0          <age>
$ # Open another terminal
$ # using watch so we can keep querying the API
$ watch 'curl <URL from minikube service list>'

$ # Introduce failure, delete any of the above displayed pods
$ kubectl delete pod version-app-dep-<uuid>
$ # You will notice the App is responsive during the deletion
$ kubectl get pods
$ # You will see pods being Terminated and New pods being created
$ # to satisfy the 3 replicas state of the system
```

### Scenario: Horizontal scaling

Remove any existing pods and service that we might have create:
```bash
$ kubectl delete -f versionApp-dep.yaml -f versionApp-svc.yaml
```

To verify horizontal scaling:
```bash
$ kubectl run py-ver-app --image=pyphercises/app:v3.0.0 --replicas=3 --port=5000
deployment "py-ver-app" created
$ kubectl expose deploy py-ver-app --port 5000 --type NodePort
service "py-ver-app" exposed
$ kubectl get pods
# Number of py-ver-app-<uuid> pods should be 3
$ kubectl scale deploy py-ver-app --replicas=4
deployment "py-ver-app" scaled

$ kubectl get pods
# Number of py-ver-app-<uuid> pods should be 4
```


### Scenario: Rolling upgrade
To build the latest version of the pyphercises application:
```bash
$ cd /path/to/pyphercises/repo/
$ make build-latest
```

To verify that the image is built and hosted on the local Docker repo:
```bash
$ docker images | grep pyphercises/app
pyphercises/app    v3.0.0    <ID>    <Time of creation>    <Size>
pyphercises/app    v4.0.0    <ID>    <Time of creation>    <Size>
```

Now to do a rolling upgrade, make sure you are querying the app:
```bash
$ # Open another terminal
$ # using watch so we can keep querying the API
$ minikube service list
....
$ | default     | py-ver-app           | http://<some IP>:<port> |
...
$ watch 'curl <URL from minikube service list>'
```

In the terminal where we were working with the local Docker repo:
```bash
$ kubectl set image deploy py-ver-app py-ver-app=pyphercises/app:v4.0.0 --record
deployment "py-ver-app" image updated

$ # If you are also watching the pods in parallel you will notice
$ # Pods getting deleted and being re created but the endpoint is always
$ # responsive
```