## Google Drive Backup Docker Image for Service Account Clients

This Dockerfile creates an image that allows you to run a Python script for backing up files to Google Drive using the Google Drive API.

### Changes to be made before running

- Make sure to make the folder you want to upload is publicly accessible and where anyone with the link is an editor.
- Get the <folder-id> by creating a folder where you want the data backed up and then get the tag after folder (as shown in `folder-id.png`)
- Replace <tags> in main.py to the required fields as given in comments.

### Run pyton file
  ```bash
  python main.py
  ```

### Prerequisites to Dokcerize the file

Before building and running the Docker image, make sure you have the following:

- Docker installed on your system.
- `main.py` and `credentials.json` files in the same directory as this Dockerfile.
- Python script (`main.py`) for Google Drive backup.

### Usage
- Build the container
  ```bash
  docker build -t <image_name> .
  ```
- Run the container
  ```bash
  docker run -d <image_name>
  ```
### Kubernetes using Cronjob and PVC to Backup folder at frequent time intervals
- Make sure to make changes to the `cronjob.yaml` file before executing.
- Have Kubernetes installed on docker.
- Make sure the container is created and uploaded to docker registry.

### To push container to docker registry
```bash
docker login
```
```bash
docker tag <container-name> <your docker user name>/<container-name>
```
```bash
docker push <your docker user name>/<container-name>
```

### To create and run a cronjob on Kubernetes
```bash
kubectl apply -f cronjob.yaml
```
### To get information about the cronjob
```bash
kubectl get cronjobs
```
### To get information about the pods running
```bash
kubectl get pods
```
### To get logs 
```bash
kubectl logs <pod-name>
```
### To delete cronjob
```bash
kubectl delete cronjob drive-backup
```
