## dependencies:
- minikube (gke version 1.15)
- helm2
- skaffold
- docker

only k8s version < 1.16 compatible with helm 2
`minikube start --kubernetes-version v1.15.0`

configure minikube to use local docker cache 
`eval $(minikube docker-env)`

configure tiller, the server-component of helm
```
kubectl -n kube-system create serviceaccount tiller                          
kubectl create=clusterrolebinding tiller \
  --clusterrole=cluster-admin \
  --serviceaccount=kube-system:tiller
helm init --service-account tiller 
```

run this in the directory where skaffold.yaml is in
skaffold watches files and will rebuild & redeploy when it detects changes 
`skaffold dev` OR
`skaffold run`

get pods running
`kubectl get po`

to tail logs from any service
`kubectl logs <name of pod> -f`

once done testing, press ctrl-c to end session and cleanup deployed resources.

#####
PROD
#####
```
gcloud init
gcloud components update
gcloud auth login

gcloud container clusters get-credentials  trippin-cluster --zone us-central1-a --project bubbly-delight-268221

gcloud auth configure-docker

kubectx gke_bubbly-delight-268221_us-central1-a_trippin-cluster

# image will be built & pushed to gcp automatically on merge to master

# for manual builds of image
$TAG=v0.0.1
$LOCAL_IMAGE_NAME=trippin:$TAG
$REPO_IMAGE_NAME=us.gcr.io/bubbly-delight-268221/trippin:$TAG
docker build -t $LOCAL_IMAGE_NAME .
docker tag $LOCAL_IMAGE_NAME $REPO_IMAGE_NAME
docker push $REPO_IMAGE_NAME
gcloud container images list-tags us.gcr.io/bubbly-delight-268221/trippin
```

update `values.yaml` with repository value to use updated image
