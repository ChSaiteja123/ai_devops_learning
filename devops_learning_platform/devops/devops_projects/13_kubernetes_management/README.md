# Kubernetes Management Project

This project demonstrates practical Kubernetes day-2 management for a small application namespace.

## Included resources

- Namespace
- Service account and least-privilege RBAC
- ConfigMap
- ResourceQuota and LimitRange
- Deployment with probes and rolling updates
- Service
- HorizontalPodAutoscaler
- PodDisruptionBudget
- NetworkPolicy

## Apply

```powershell
kubectl apply -f namespace.yaml
kubectl apply -f rbac.yaml
kubectl apply -f config.yaml
kubectl apply -f policies.yaml
kubectl apply -f workload.yaml
kubectl apply -f service.yaml
kubectl apply -f autoscaling.yaml
kubectl -n platform-demo get all
```

## Operate

```powershell
kubectl -n platform-demo rollout status deployment/platform-api
kubectl -n platform-demo get events --sort-by=.lastTimestamp
kubectl -n platform-demo top pods
kubectl -n platform-demo rollout history deployment/platform-api
kubectl -n platform-demo rollout undo deployment/platform-api
```

Review and adapt image names, resource limits, storage, ingress, authentication, and cluster policy before production use.
