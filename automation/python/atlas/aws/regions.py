from typing import Any

import boto3


def get_all_regions(
    session: boto3.Session,
) -> list[dict[str, Any]]:
    """Return all AWS regions, including regions requiring opt-in."""
    ec2 = session.client(
        "ec2",
        region_name=session.region_name or "us-east-1",
    )

    response = ec2.describe_regions(AllRegions=True)

    return sorted(
        response["Regions"],
        key=lambda region: region["RegionName"],
    )


def get_enabled_regions(session: boto3.Session) -> list[str]:
    """Return regions available for use by the current AWS account."""
    enabled_statuses = {
        "opt-in-not-required",
        "opted-in",
    }

    return [
        region["RegionName"]
        for region in get_all_regions(session)
        if region.get("OptInStatus") in enabled_statuses
    ]