# Istio Service Mesh Project

This project demonstrates Istio traffic management and security for a small Kubernetes service.

## Concepts

- Istio ingress Gateway
- VirtualService routing
- DestinationRule subsets
- traffic shifting between versions
- retries and timeouts
- PeerAuthentication mTLS
- telemetry and sidecar injection

## Prerequisites

- Kubernetes cluster
- Istio installed with the `istio-ingressgateway` service
- `istioctl` available

## Apply

```powershell
kubectl apply -f namespace.yaml
kubectl apply -f workload.yaml
kubectl apply -f traffic.yaml
kubectl apply -f security.yaml
kubectl -n mesh-demo get pods
kubectl -n mesh-demo get virtualservice,destinationrule
```

## Verify

```powershell
istioctl analyze -n mesh-demo
kubectl -n mesh-demo get gateway,virtualservice
kubectl -n mesh-demo describe peerauthentication default
```

The image names are placeholders. Replace them with approved images before deployment. Start with a small canary percentage and monitor error rate, latency, and saturation before increasing traffic.
