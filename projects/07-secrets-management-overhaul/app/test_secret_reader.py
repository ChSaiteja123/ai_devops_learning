import json
from unittest.mock import Mock

import pytest

from secret_reader import read_secret


def test_reads_json_secret_without_exposing_value(capsys):
    client = Mock()
    client.get_secret_value.return_value = {
        "SecretString": json.dumps({"username": "demo", "password": "not-a-real-password"})
    }

    result = read_secret("test/app", "ap-south-1", client)

    assert result["username"] == "demo"
    client.get_secret_value.assert_called_once_with(SecretId="test/app")
    assert capsys.readouterr().out == ""


def test_rejects_empty_secret_id():
    with pytest.raises(ValueError, match="secret_id"):
        read_secret("", "ap-south-1", Mock())
