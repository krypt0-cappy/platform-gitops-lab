from typing import Any

import boto3


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
            }
        )

    return sorted(
        buckets,
        key=lambda bucket: bucket["bucket_name"],
    )