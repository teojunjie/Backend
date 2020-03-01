#!/bin/bash

set -euo pipefail

pip install envsubst

# Create Service Account
echo "Create Service Account for GCloud authentication"``
cat >> service-account.json << EOF
{
  "type": "service_account",
  "project_id": "$GCLOUD_PROJECT_ID",
  "private_key_id": "$GCLOUD_PRIVATE_KEY_ID",
  "private_key": "$GCLOUD_PRIVATE_KEY",
  "client_email": "$GCLOUD_EMAIL",
  "client_id": "$GCLOUD_CLIENT_ID",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "$GCLOUD_CERT_URL"
}
EOF

# GCloud Authentication
gcloud auth activate-service-account --key-file=service-account.json

# Connect to Cluster
echo '>' gcloud container clusters get-credentials $KUBERNETES_CLUSTER_NAME --zone $KUBERNETES_CLUSTER_ZONE --project $GCLOUD_PROJECT_ID
gcloud container clusters get-credentials $KUBERNETES_CLUSTER_NAME --zone $KUBERNETES_CLUSTER_ZONE --project $GCLOUD_PROJECT_ID

# Install kubectl
echo '>' apt-get install kubectl
apt-get install kubectl

# Kubernetes Deployment
echo '>' kubectl apply -f config/kube/deployment.yaml
envsubst < config/kube/deployment.yaml | kubectl apply -f -

# Kubernetes Service
echo '>' kubectl apply -f config/kube/service.yaml
kubectl apply -f config/kube/service.yaml

# Kubernetes Ingress
echo '>' kubectl apply -f config/kube/ingress.yaml
envsubst < config/kube/ingress.yaml | kubectl apply -f -

# Kubernetes Service
# echo '>' kubectl apply -f config/kube/service.yaml
# kubectl apply -f config/kube/service.yaml

# Remove the service account
echo 'Remove Service Account'
rm service-account.json