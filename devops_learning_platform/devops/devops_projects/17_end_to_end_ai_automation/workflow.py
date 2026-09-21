import json
import sys
from datetime import datetime, timezone
from pathlib import Path


REQUIRED_INCIDENT_FIELDS = {"incident_id", "alert", "recent_deployment"}
ALLOWED_SEVERITIES = {"info", "warning", "critical"}


def validate_incident(incident, policy):
    missing = REQUIRED_INCIDENT_FIELDS.difference(incident)
    if missing:
        raise ValueError(f"missing incident fields: {sorted(missing)}")
    alert = incident["alert"]
    for field in ("fingerprint", "service", "environment", "severity", "summary", "runbook"):
        if not alert.get(field):
            raise ValueError(f"missing alert field: {field}")
    if alert["severity"] not in ALLOWED_SEVERITIES:
        raise ValueError(f"unsupported severity: {alert['severity']}")
    if "allowed_actions" not in policy or "blocked_actions" not in policy:
        raise ValueError("policy must define allowed and blocked actions")


def analyze_incident(incident):
    deployment = incident["recent_deployment"]
    likely_change_related = deployment["minutes_ago"] <= 15
    return {
        "hypothesis": "recent deployment may be related" if likely_change_related else "correlation is unconfirmed",
        "confidence": "medium" if likely_change_related else "low",
        "evidence": [
            f"service={incident['alert']['service']}",
            f"severity={incident['alert']['severity']}",
            f"deployment_minutes_ago={deployment['minutes_ago']}",
        ],
        "recommended_actions": ["inspect_dashboard", "create_incident", "prepare_rollback"],
        "automated_action": False,
    }


def apply_policy(incident, analysis, policy):
    approved_actions = [
        action for action in analysis["recommended_actions"]
        if action in policy["allowed_actions"] and action not in policy["blocked_actions"]
    ]
    requires_approval = (
        incident["alert"]["severity"] == "critical"
        and policy["critical_requires_approval"]
    )
    return {
        "approved_actions": approved_actions,
        "requires_human_approval": requires_approval,
        "decision": "awaiting_approval" if requires_approval else "dry_run_ready",
    }


def build_audit(incident, analysis, decision):
    deployment = incident["recent_deployment"]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "incident_id": incident["incident_id"],
        "service": incident["alert"]["service"],
        "environment": incident["alert"]["environment"],
        "model_mode": "deterministic_local_analysis",
        "analysis": analysis,
        "policy_decision": decision,
        "deployment_plan": {
            "target": deployment["version"],
            "rollback_target": deployment["previous_version"],
            "executed": False,
        },
        "audit_status": "complete",
    }


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python workflow.py incident.json")
    root = Path(__file__).parent
    incident = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    policy = json.loads((root / "policy.json").read_text(encoding="utf-8"))
    validate_incident(incident, policy)
    analysis = analyze_incident(incident)
    decision = apply_policy(incident, analysis, policy)
    audit = build_audit(incident, analysis, decision)
    Path("automation-audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
