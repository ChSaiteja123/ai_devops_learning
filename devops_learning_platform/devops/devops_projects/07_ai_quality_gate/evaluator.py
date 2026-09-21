import json
from pathlib import Path


REQUIRED_FIELDS = {"severity", "finding", "recommendation"}
ALLOWED_SEVERITIES = {"low", "medium", "high", "critical"}


def validate_findings(findings):
    if not isinstance(findings, list):
        raise ValueError("findings must be a list")

    for finding in findings:
        if not isinstance(finding, dict):
            raise ValueError("each finding must be an object")
        if not REQUIRED_FIELDS.issubset(finding):
            raise ValueError("finding is missing required fields")
        if finding["severity"] not in ALLOWED_SEVERITIES:
            raise ValueError("finding has an invalid severity")


def run_evaluation():
    findings = [
        {
            "severity": "high",
            "finding": "Generated code should be reviewed before execution.",
            "recommendation": "Require tests and human approval before merge.",
        }
    ]
    validate_findings(findings)
    return {
        "passed": True,
        "finding_count": len(findings),
        "critical_count": sum(item["severity"] == "critical" for item in findings),
    }


def main():
    report = run_evaluation()
    Path("evaluation-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
