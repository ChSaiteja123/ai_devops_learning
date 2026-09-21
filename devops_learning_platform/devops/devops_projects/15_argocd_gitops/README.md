# Argo CD GitOps Project

This project demonstrates declarative Kubernetes delivery with Argo CD.

Argo CD watches the Git repository path configured in `application.yaml` and reconciles the target cluster to the manifests stored there.

## Prerequisites

- Kubernetes cluster
- Argo CD installed in the `argocd` namespace
- Git repository containing the application manifests
- `argocd` CLI or access to the Argo CD UI

## Configure

Replace the placeholder repository URL in `application.yaml` and commit the application manifests to the configured path.

## Apply

```powershell
kubectl apply -f application.yaml
kubectl -n argocd get applications
argocd app get platform-api
argocd app sync platform-api
```

The Application uses automated sync, pruning, and self-healing. Keep production repository branches protected and use pull-request review as the change approval boundary.
