# End-to-End AI DevOps Automation

This project connects an operational alert to an AI-assisted incident analysis, a policy gate, a dry-run deployment plan, and an audit report.

## End-to-end flow

```text
Alert -> validate -> deduplicate -> AI analysis -> policy gate -> approval decision
-> dry-run remediation plan -> audit evidence -> deploy through a separate authorized job
```

The implementation is deterministic and provider-free by default. The `analyze_incident` function is the safe replacement point for an approved model adapter, but model output must remain advisory until policy and authorization checks pass.

## Run

```powershell
python workflow.py incident.json
```

The command writes `automation-audit.json` and never changes a cluster, sends a notification, or executes a rollback.

## Production extension points

- replace deterministic analysis with an approved provider adapter
- validate model output with a schema
- add prompt-injection and red-team test cases
- connect incident creation and notification APIs
- require human approval for production changes
- create a separate signed deployment job with least-privilege credentials
- store audit evidence in protected immutable storage
- add cost, latency, model-version, and quality telemetry
