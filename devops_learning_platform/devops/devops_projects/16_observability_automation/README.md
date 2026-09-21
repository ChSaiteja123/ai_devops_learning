# Observability Automation

This project demonstrates an alert-processing automation service for Prometheus and Alertmanager.

It accepts an Alertmanager-style JSON payload, validates alerts, groups related events, deduplicates fingerprints, assigns notification routes, and writes an auditable action plan.

## Run locally

```powershell
python alert_router.py sample-alerts.json
```

The default behavior is dry-run only. It creates `notification-plan.json` and does not send messages or change infrastructure.

## Included files

- `alert_router.py`: validation, grouping, routing, and audit output
- `sample-alerts.json`: Alertmanager-style test payload
- `prometheus.yml`: scrape and Alertmanager connection example
- `alertmanager.yml`: severity-based receiver routes
- `alerts.yml`: sample service alerts
- `Jenkinsfile`: syntax and behavior validation

## Production safeguards

- authenticate webhook requests
- verify Alertmanager identity and payload signatures where supported
- deduplicate using stable fingerprints
- use bounded retries and a dead-letter path
- do not execute remediation directly from an alert payload
- require authorization and human approval for high-impact actions
- redact secrets and personal data from notifications
- store audit records with retention and access controls
