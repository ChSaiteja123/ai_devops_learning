import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


REQUIRED_LABELS = {"alertname", "service", "severity", "environment"}
SEVERITY_ORDER = {"info": 1, "warning": 2, "critical": 3}
RECEIVERS = {
    "critical": "on-call-pager",
    "warning": "platform-ticketing",
    "info": "observability-digest",
}


def validate_alert(alert):
    labels = alert.get("labels", {})
    missing = REQUIRED_LABELS.difference(labels)
    if missing:
        raise ValueError(f"missing labels: {sorted(missing)}")
    if labels["severity"] not in SEVERITY_ORDER:
        raise ValueError(f"unsupported severity: {labels['severity']}")
    if not alert.get("fingerprint"):
        raise ValueError("alert fingerprint is required")


def process_payload(payload):
    if not isinstance(payload.get("alerts"), list):
        raise ValueError("payload must contain an alerts list")

    grouped = defaultdict(list)
    seen = set()
    duplicate_count = 0
    for alert in payload["alerts"]:
        validate_alert(alert)
        fingerprint = alert["fingerprint"]
        if fingerprint in seen:
            duplicate_count += 1
            continue
        seen.add(fingerprint)
        labels = alert["labels"]
        key = (labels["environment"], labels["severity"])
        grouped[key].append(alert)

    groups = []
    for (environment, severity), alerts in sorted(
        grouped.items(), key=lambda item: SEVERITY_ORDER[item[0][1]], reverse=True
    ):
        groups.append(
            {
                "environment": environment,
                "severity": severity,
                "receiver": RECEIVERS[severity],
                "alert_count": len(alerts),
                "alertnames": sorted({item["labels"]["alertname"] for item in alerts}),
                "services": sorted({item["labels"]["service"] for item in alerts}),
                "runbooks": sorted({item.get("annotations", {}).get("runbook_url", "") for item in alerts if item.get("annotations", {}).get("runbook_url")}),
                "automated_notification_sent": False,
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_status": payload.get("status", "unknown"),
        "unique_alert_count": len(seen),
        "duplicate_count": duplicate_count,
        "groups": groups,
    }


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python alert_router.py sample-alerts.json")
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    plan = process_payload(payload)
    Path("notification-plan.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()
