import argparse
import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import boto3


def recent_backup_jobs(
    backup: Any, since: datetime, until: datetime
) -> list[dict[str, str]]:
    jobs: list[dict[str, str]] = []
    paginator = backup.get_paginator("list_backup_jobs")
    for page in paginator.paginate(ByCreatedAfter=since, ByCreatedBefore=until):
        for job in page.get("BackupJobs", []):
            created = job.get("CreationDate")
            jobs.append(
                {
                    "backup_job_id": job.get("BackupJobId", "unknown"),
                    "resource_type": job.get("ResourceType", "unknown"),
                    "resource_arn": job.get("ResourceArn", "unknown"),
                    "state": job.get("State", "unknown"),
                    "created_at": created.isoformat() if created else "unknown",
                    "recovery_point_arn": job.get("RecoveryPointArn", "unknown"),
                }
            )
    return jobs


def write_report(jobs: list[dict[str, str]], destination: Path) -> None:
    fields = [
        "backup_job_id",
        "resource_type",
        "resource_arn",
        "state",
        "created_at",
        "recovery_point_arn",
    ]
    with destination.open("w", newline="", encoding="utf-8") as report:
        writer = csv.DictWriter(report, fieldnames=fields)
        writer.writeheader()
        writer.writerows(jobs)


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only AWS Backup job inventory.")
    parser.add_argument("--region", required=True, help="AWS region to inspect")
    parser.add_argument("--hours", type=int, default=168, help="Lookback window (default: 7 days)")
    parser.add_argument("--output", type=Path, default=Path("backup-jobs.csv"))
    args = parser.parse_args()
    if args.hours < 1:
        parser.error("--hours must be at least 1")

    now = datetime.now(timezone.utc)
    session = boto3.Session(region_name=args.region)
    jobs = recent_backup_jobs(
        session.client("backup"),
        now - timedelta(hours=args.hours),
        now,
    )
    write_report(jobs, args.output)
    print(f"Wrote {len(jobs)} backup job(s) to {args.output}")


if __name__ == "__main__":
    main()
