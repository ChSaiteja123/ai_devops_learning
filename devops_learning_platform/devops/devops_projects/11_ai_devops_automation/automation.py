import json
import sys
from datetime import datetime, timezone
from pathlib import Path


REQUIRED_FIELDS = {"alert_id", "service", "severity", "symptom", "environment", "owner"}
SEVERITY_ORDER = {"info": 1, "warning": 2, "critical": 3}


def validate_alert(alert):
    missing = REQUIRED_FIELDS.difference(alert)
    if missing:
        raise ValueError(f"missing alert fields: {sorted(missing)}")
    if alert["severity"] not in SEVERITY_ORDER:
        raise ValueError(f"unknown severity: {alert['severity']}")


def recommend_actions(alert):
    severity = alert["severity"]
    actions = [
        f"Notify the {alert['owner']} owner.",
        f"Open an incident record for {alert['service']}.",
        "Inspect the latest deployment and service dashboard.",
    ]
    if severity == "critical":
        actions.append("Request human approval before rollback or traffic changes.")
    elif severity == "warning":
        actions.append("Review queue and dependency health before escalation.")
    else:
        actions.append("Track the signal without paging the on-call engineer.")
    return actions


def build_report(alerts):
    for alert in alerts:
        validate_alert(alert)

    ordered = sorted(
        alerts,
        key=lambda alert: SEVERITY_ORDER[alert["severity"]],
        reverse=True,
    )
    incidents = []
    for alert in ordered:
        incidents.append(
            {
                "alert_id": alert["alert_id"],
                "priority": alert["severity"],
                "summary": (
                    f"{alert['service']} in {alert['environment']}: "
                    f"{alert['symptom']}"
                ),
                "actions": recommend_actions(alert),
                "automated_action_taken": False,
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "incident_count": len(incidents),
        "incidents": incidents,
    }


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python automation.py alerts.json")

    alerts = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    report = build_report(alerts)
    Path("incident-report.json").write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
