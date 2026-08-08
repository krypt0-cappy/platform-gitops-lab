from typing import Any

import boto3
from botocore.exceptions import ClientError


####################
#### GET REGION ####
####################
def get_bucket_region(
    s3: Any,
    bucket_name: str,
) -> str:
    try:
        response = s3.get_bucket_location(
            Bucket=bucket_name,
        )
    except ClientError:
        return "unknown"

    location = response.get("LocationConstraint")

    if location is None:
        return "us-east-1"

    if location == "EU":
        return "eu-west-1"

    return location


########################
#### GET VERSIONING ####
########################
def get_versioning_status(
    s3: Any,
    bucket_name: str,
) -> str:
    response = s3.get_bucket_versioning(
        Bucket=bucket_name,
    )

    return response.get("Status", "Disabled")


########################
#### GET ENCRYPTION ####
########################
def get_encryption_status(
    s3: Any,
    bucket_name: str,
) -> str:
    try:
        response = s3.get_bucket_encryption(
            Bucket=bucket_name,
        )
    except ClientError as error:
        error_code = error.response["Error"]["Code"]

        if error_code == "ServerSideEncryptionConfigurationNotFoundError":
            return "Not configured"

        return "unknown"

    rules = response.get(
        "ServerSideEncryptionConfiguration",
        {},
    ).get("Rules", [])

    if not rules:
        return "Not configured"

    encryption = rules[0].get(
        "ApplyServerSideEncryptionByDefault",
        {},
    )

    return encryption.get(
        "SSEAlgorithm",
        "Configured",
    )


###########################
#### GET PUBLIC ACCESS ####
###########################
def get_public_access_block_status(
    s3: Any,
    bucket_name: str,
) -> str:
    try:
        response = s3.get_public_access_block(
            Bucket=bucket_name,
        )
    except ClientError as error:
        error_code = error.response["Error"]["Code"]

        if error_code == "NoSuchPublicAccessBlockConfiguration":
            return "Not configured"

        return "unknown"

    configuration = response["PublicAccessBlockConfiguration"]

    settings = [
        configuration.get("BlockPublicAcls", False),
        configuration.get("IgnorePublicAcls", False),
        configuration.get("BlockPublicPolicy", False),
        configuration.get("RestrictPublicBuckets", False),
    ]

    if all(settings):
        return "Fully blocked"

    if any(settings):
        return "Partially blocked"

    return "Not blocked"


#####################
#### GET BUCKETS ####
#####################
def collect_buckets(
    session: boto3.Session,
) -> list[dict[str, Any]]:

    s3 = session.client("s3")

    response = s3.list_buckets()

    buckets: list[dict[str, Any]] = []

    for bucket in response.get("Buckets", []):

        print(f"Scanning {bucket['Name']}...")

        buckets.append(
            {
                "bucket_name": bucket["Name"],
                "creation_date": bucket["CreationDate"].isoformat(),
                "region": get_bucket_region(
                    s3,
                    bucket["Name"],
                ),
                "versioning": get_versioning_status(
                    s3,
                    bucket["Name"],
                ),
                "encryption": get_encryption_status(
                    s3,
                    bucket["Name"],
                ),
                "public_access_block": get_public_access_block_status(
                    s3,
                    bucket["Name"],
                ),
            }
        )

    return sorted(
        buckets,
        key=lambda bucket: bucket["bucket_name"],
    )
