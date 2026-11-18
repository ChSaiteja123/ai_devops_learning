import json
import os
from typing import Any

import boto3


def read_secret(secret_id: str, region: str, client: Any = None) -> dict[str, Any]:
    if not secret_id:
        raise ValueError("secret_id must not be empty")
    secrets = client or boto3.client("secretsmanager", region_name=region)
    response = secrets.get_secret_value(SecretId=secret_id)
    secret_string = response.get("SecretString")
    if not secret_string:
        raise ValueError("Secret has no SecretString; binary secrets are not supported by this example")
    parsed = json.loads(secret_string)
    if not isinstance(parsed, dict):
        raise ValueError("SecretString must contain a JSON object")
    return parsed


def main() -> None:
    secret_id = os.environ.get("APP_SECRET_ID", "")
    region = os.environ.get("AWS_REGION", "ap-south-1")
    secret = read_secret(secret_id, region)
    # Do not log or print secret values. This sample confirms retrieval only.
    print(f"Successfully retrieved configured secret with {len(secret)} field(s).")


if __name__ == "__main__":
    main()
