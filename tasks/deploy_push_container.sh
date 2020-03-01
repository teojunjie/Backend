#!/bin/bash

set -euo pipefail

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


# Login to Google Cloud Registry
cat service-account.json | docker login -u _json_key --password-stdin https://$CONTAINER_REGISTRY

# Build container
pipenv lock -r > requirements.txt
echo '>' docker build -t $CONTAINER_REGISTRY/$GCLOUD_PROJECT_ID/$CONTAINER_IMAGENAME:$ENV .
docker build -t $CONTAINER_REGISTRY/$GCLOUD_PROJECT_ID/$CONTAINER_IMAGENAME:$ENV .

# Push container
echo '>' docker push $CONTAINER_REGISTRY/$GCLOUD_PROJECT_ID/$CONTAINER_IMAGENAME:$ENV
docker push $CONTAINER_REGISTRY/$GCLOUD_PROJECT_ID/$CONTAINER_IMAGENAME:$ENV

# Remove the service account
echo 'Remove Service Account'
rm service-account.json