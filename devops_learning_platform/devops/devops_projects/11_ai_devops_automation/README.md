# AI DevOps Incident Automation

This project demonstrates a safe automation pattern for AI-assisted DevOps incident triage.

The local implementation is deterministic and does not call an external AI provider. It reads alert events, classifies severity, recommends bounded remediation steps, and writes an audit report.

## Run

```powershell
python automation.py alerts.json
```

## Workflow

1. Read structured alerts.
2. Validate required fields.
3. Classify incident priority.
4. Generate a concise incident summary.
5. Recommend safe, non-destructive actions.
6. Write `incident-report.json`.

## Production extensions

- replace the deterministic classifier with an approved model adapter
- keep authorization and remediation execution outside the model
- require human approval before destructive actions
- add PagerDuty, Slack, or ticket integrations
- redact secrets and personal data
- store audit records immutably
- add evaluation cases for prompt injection and unsafe recommendations
