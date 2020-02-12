# Getting Started
## *Prerequisites*
#### Google Cloud Platform
***
1) Create a new project in [GCP](https://console.cloud.google.com/projectselector2/home/dashboard) (Google Cloud Platform)
2) [Install](https://cloud.google.com/sdk/docs/) and initialize the Cloud SDK
3) Enable the [APIs](https://console.cloud.google.com/flows/enableapi?apiid=datastore.googleapis.com,pubsub,storage_api,logging,plus)
4) Install python from their website[https://www.python.org/downloads/windows/]
#### Powershell:
***
##### Follow the instructions below
1) Run '`Set-ExecutionPolicy Unrestricted`'
2) Check to see if python and pip is installed and you have the latest version with `python --version` and `pip --version`
3) cd <project_directory>
4) Run `py -m venv <name_of_virtual_env>` to create a python virtual environment to isolate dependencies
5) Run `./<name_of_virtual_env>/Scripts/activate` to activate virtual environment
6) Run `pip install -r requirements.txt`

## *Creating the django application*
---
1) Create a django project in your project directory
2) Run `django-admin startproject base_app`
3) Run `Rename-item -Path "base_app" -NewName "code"` to rename the django project
4) Run `cd code`
5) Run `python manage.py runserver` and visit [here](http://127.0.0.1:8000/) to view your site if you set up everything properly
6) Right-click [here](https://dl.google.com/cloudsql/cloud_sql_proxy_x64.exe) and select Save Link As to download the proxy. Rename the file to cloud_sql_proxy.exe
***
#### Gcloud
1) Run `gcloud services enable sqladmin`
2) Create a Cloud SQL for PostgresSQL instance [here](https://cloud.google.com/sql/docs/postgres/create-instance)
    - instance_name = <project_name>-cloud-sql-instance
    - user: postgres
    - password: postgres

3) Run `gcloud sql instances describe <instance_name>` and take note of the value of the `connectionName`
4) `CONNECTION_NAME` is in the format `[PROJECT_NAME]:[REGION_NAME]:[INSTANCE_NAME]`
5) Run `cloud_sql_proxy.exe -instances="<INSTANCE_CONNECTION_NAME>"=tcp:5432`
***
#### Creating the Cloud SQL database instance
1) Create a database in the Cloud SQL instance [page](https://console.cloud.google.com/sql/instances)
2) Select the databases tab
3) Click create database
4) Specify the name of the database and create it
    - database_name = <project_name>-database

5) Create a service account [here](https://console.cloud.google.com/iam-admin/serviceaccounts/)
6) Select the project that contains your Cloud SQL instance
7) Click create service account
8) Provide a descriptive name of the service account
9) For role, select cloud sql admin
    - service_account_name = <project_name>-service-account
10) Create a new private key and confirm the key type is `JSON` and save it locally

11) Set the environment variables for the database access for local testing
    - Windows CMD
        - Run `set DATABASE_USER=<your-database-user>`
        - Run `set DATABASE_PASSWORD=<your-database-password>`
        - To print it, run `echo %VAR_NAME%`

    - Windows Powershell
        - Run `$env:VAR_NAME="VALUE"`
        - To print it, use `$env:VAR_NAME`
***
#### Setting up the GKE(Google Kubernetes Engine) configuration
1) The application is represented in a single Kubernetes configuration called trippin
2) In trippin.yaml, replace <your-project-id> with your google cloud project ID
***
#### Starting your local environment
1) Start your virtual env and install any additional requirements
2) Run `python manage.py makemigrations`
3) Run `python manage.py migrate`
4) Install dbeaver and connect to database with the following credentials
    - database_name=\<project>-database
    - user=postgres
    - password=postgres
    - host: 127.0.0.1 (Uses the Cloud SQL Proxy, thats why its resolving to localhost at port 5432)
    - port: 5432

5) Create a django super user with the command `python manage.py createsuperuser`
6) Run the main program with `python manage.py runserver`
7) Test if you can log in with your super user account
***
#### Create a google cloud storage bucket
1) bucket_name=\<project>-bucket
2) set public read for the bucket with `gsutil defacl set public-read gs://[YOUR_GCS_BUCKET]`
3) collect all the static files with `python manage.py collectstatic`
4) Replace `STATIC_URL` of `mysite/settings.py` with the following `http://storage.googleapis.com/[YOUR_GCS_BUCKET]/static/`
5) Synchronize the data locally in the static folder with the bucket with `gsutil rsync -R static/ gs://[YOUR_GCS_BUCKET]/static`
***

#### Setting up google kubernetes engine
1) To initialize GKE, go to the [Clusters](https://console.cloud.google.com/kubernetes/list) page
2) Create a cluster with `gcloud container clusters create <project_name> --scopes "https://www.googleapis.com/auth/userinfo.email","cloud-platform" --num-nodes 4 --zone "us-central1-a"`

#### Using docker and kubernetes
1) Install Docker Toolbox [here](https://github.com/docker/toolbox/releases) with the latest .exe release
2) Install curl [here](https://curl.haxx.se/download.html) or with choco `choco install curl`
3) Install kubernetes [here](https://kubernetes.io/docs/tasks/tools/install-kubectl/) or with curl 
    - `curl https://storage.googleapis.com/kubernetes-release/release/v1.17.0/bin/windows/amd64/kubectl.exe`

4) Make sure that kubectl is configured to interact with the right cluster (context)
5) Run `gcloud container clusters get-credentials <project_name> --zone "us-central1-a"`
6) Create secrets to enable your GKE app to connect with your Cloud SQL instance.
    - Instance level access connection
        - Run the following command 
            - `kubectl create secret generic cloudsql-oauth-credentials --from-file=credentials.json=[PATH_TO_CREDENTIAL_FILE]`
    - Database access
        - Run the following command
            - `kubectl create secret generic cloudsql --from-literal=username=[PROXY_USERNAME] --from-literal=password=[PASSWORD]`
7) Check to see if the secrets are there with `kubectl get secrets`
8) If you done it correctly you should see 
    - cloudsql
    - cloudsql-oauth-credentials


9) Retrieve the public Docker image for the Cloud SQL proxy with `docker pull b.gcr.io/cloudsql-docker/gce-proxy`
10) Build the image with `docker build -t gcr.io/<your-project-id>/<project_name> .`
11) Configure docker with `gcloud auth configure-docker`
12) Push to container registry with `docker push gcr.io/<your-project-id>/<project_name>`
13) You can visit the container registry of your project [here](https://cloud.google.com/container-registry/)
14) Finally create the resource
15) Run `kubectl create -f <project_name>.yaml`
16) Check to see if your pods are running with `kubectl get pods`
17) Check to see if the service is running with `kubectl get services`