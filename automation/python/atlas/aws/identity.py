from typing import Any

import boto3


def get_identity(session: boto3.Session) -> dict[str, Any]:
    """Return the identity associated with the active AWS credentials."""
    sts = session.client("sts")
    return sts.get_caller_identity()
