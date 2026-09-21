# AI Quality Gate

A dependency-free AI evaluation project for CI. It validates structured findings and fails when a critical finding is missing required fields.

## Run

```powershell
python evaluator.py
```

## Jenkins

The `Jenkinsfile` runs the evaluator and archives `evaluation-report.json`.

This project uses a deterministic mock response. Replace the mock response with a provider adapter only after adding secret management, timeouts, output validation, cost limits, and an evaluation dataset.
