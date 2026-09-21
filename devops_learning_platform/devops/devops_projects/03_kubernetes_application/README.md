# Kubernetes Application

This folder contains a Deployment and Service for the Docker application.

Build and publish the image first, then replace `YOUR_DOCKERHUB_USER/devops-python-app:latest` in `deployment.yaml`.

## Apply

```powershell
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods
kubectl get service devops-python-app
```
