import argparse
import csv
from pathlib import Path
from typing import Any

import boto3


def stopped_instances(ec2: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    paginator = ec2.get_paginator("describe_instances")
    for page in paginator.paginate(
        Filters=[{"Name": "instance-state-name", "Values": ["stopped"]}]
    ):
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                tags = {tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])}
                findings.append(
                    {
                        "resource_type": "ec2-instance",
                        "resource_id": instance["InstanceId"],
                        "region": ec2.meta.region_name,
                        "state": instance["State"]["Name"],
                        "owner": tags.get("Owner", "unknown"),
                        "recommendation": "Review with owner; do not stop or delete automatically.",
                    }
                )
    return findings


def write_report(findings: list[dict[str, str]], destination: Path) -> None:
    fields = [
        "resource_type",
        "resource_id",
        "region",
        "state",
        "owner",
        "recommendation",
    ]
    with destination.open("w", newline="", encoding="utf-8") as report:
        writer = csv.DictWriter(report, fieldnames=fields)
        writer.writeheader()
        writer.writerows(findings)


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only report of stopped EC2 instances.")
    parser.add_argument("--region", required=True, help="AWS region to inspect")
    parser.add_argument("--output", type=Path, default=Path("findings.csv"))
    args = parser.parse_args()

    session = boto3.Session(region_name=args.region)
    findings = stopped_instances(session.client("ec2"))
    write_report(findings, args.output)
    print(f"Wrote {len(findings)} read-only finding(s) to {args.output}")


if __name__ == "__main__":
    main()
