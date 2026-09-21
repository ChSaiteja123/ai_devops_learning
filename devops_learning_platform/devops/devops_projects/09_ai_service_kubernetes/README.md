# AI Service on Kubernetes

This project provides deployment manifests for a containerized AI API. The image is intentionally a placeholder; replace it with an approved inference service image.

## Apply

```powershell
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods
kubectl get service ai-service
```

The deployment includes resource limits and a readiness probe. Add secrets, network policies, authentication, model configuration, and autoscaling before production use.
