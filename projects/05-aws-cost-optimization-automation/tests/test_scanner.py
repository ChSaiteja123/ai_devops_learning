from pathlib import Path
from unittest.mock import Mock

from src.scanner import stopped_instances, write_report


def test_stopped_instances_paginates_and_does_not_mutate():
    ec2 = Mock()
    ec2.meta.region_name = "ap-south-1"
    ec2.get_paginator.return_value.paginate.return_value = [
        {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "InstanceId": "i-example",
                            "State": {"Name": "stopped"},
                            "Tags": [{"Key": "Owner", "Value": "team-a"}],
                        }
                    ]
                }
            ]
        }
    ]

    findings = stopped_instances(ec2)

    assert findings[0]["resource_id"] == "i-example"
    assert findings[0]["owner"] == "team-a"
    assert "do not stop or delete" in findings[0]["recommendation"]
    ec2.get_paginator.assert_called_once_with("describe_instances")
    assert not any("stop" in call[0] or "terminate" in call[0] for call in ec2.method_calls)


def test_write_report_creates_header_for_empty_results(tmp_path: Path):
    output = tmp_path / "findings.csv"
    write_report([], output)
    assert "resource_id" in output.read_text(encoding="utf-8")
