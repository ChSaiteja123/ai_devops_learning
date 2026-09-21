# Automated Deployment Pipeline

This project demonstrates a safe deployment workflow for promoting an immutable container image to a Kubernetes environment.

## Workflow

```text
Validate -> Build -> Push -> Deploy -> Wait for rollout -> Smoke test -> Promote or rollback
```

## Local dry run

The deployment script prints the actions by default and does not modify a cluster:

```powershell
python deploy.py --environment staging --image registry.example.com/app:1.0.0
```

To execute real commands, use `--execute` from a trusted deployment agent with Kubernetes credentials:

```powershell
python deploy.py --environment staging --image registry.example.com/app:1.0.0 --execute
```

## Jenkins

`Jenkinsfile` demonstrates validation, image identity, deployment, rollout verification, and manual production approval.

## Production safeguards

- use immutable image digests instead of mutable tags
- separate staging and production credentials
- require approval for production
- restrict deployment service-account permissions
- verify health before completing the rollout
- keep the previous image available for rollback
- record commit, image digest, operator, and deployment result
