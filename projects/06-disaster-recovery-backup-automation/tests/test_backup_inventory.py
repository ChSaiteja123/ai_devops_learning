from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock

from src.backup_inventory import recent_backup_jobs, write_report


def test_recent_backup_jobs_paginates_and_normalizes():
    created = datetime(2026, 1, 1, tzinfo=timezone.utc)
    backup = Mock()
    backup.get_paginator.return_value.paginate.return_value = [
        {
            "BackupJobs": [
                {
                    "BackupJobId": "job-1",
                    "ResourceType": "RDS",
                    "ResourceArn": "arn:aws:rds:region:account:db:test",
                    "State": "COMPLETED",
                    "CreationDate": created,
                    "RecoveryPointArn": "arn:aws:backup:region:account:recovery-point:rp-1",
                }
            ]
        }
    ]

    jobs = recent_backup_jobs(backup, created, created)

    assert jobs[0]["backup_job_id"] == "job-1"
    assert jobs[0]["state"] == "COMPLETED"
    assert jobs[0]["created_at"] == created.isoformat()
    backup.get_paginator.assert_called_once_with("list_backup_jobs")


def test_write_report_handles_no_jobs(tmp_path: Path):
    output = tmp_path / "jobs.csv"
    write_report([], output)
    assert "backup_job_id" in output.read_text(encoding="utf-8")
