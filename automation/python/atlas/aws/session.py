import os

import boto3


def get_session() -> boto3.Session:
    """Create an AWS session using AWS_PROFILE when it is configured."""
    profile = os.getenv("AWS_PROFILE")

    if profile:
        return boto3.Session(profile_name=profile)

    return boto3.Session()
