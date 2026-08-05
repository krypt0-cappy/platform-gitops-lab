from typing import Any

import boto3


def get_name_tag(
    tags: list[dict[str, str]] | None,
) -> str:
    """Return the value of the EC2 Name tag when one exists."""
    if not tags:
        return ""

    for tag in tags:
        if tag.get("Key") == "Name":
            return tag.get("Value", "")

    return ""


def collect_instances(
    session: boto3.Session,
    regions: list[str],
) -> list[dict[str, Any]]:
    """Collect EC2 instances from each supplied AWS region."""
    instances: list[dict[str, Any]] = []

    for region in regions:
        print(f"Scanning {region}...")

        ec2 = session.client("ec2", region_name=region)
        paginator = ec2.get_paginator("describe_instances")

        for page in paginator.paginate():
            for reservation in page.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    instances.append(
                        {
                            "region": region,
                            "instance_id": instance["InstanceId"],
                            "name": get_name_tag(instance.get("Tags")),
                            "state": instance["State"]["Name"],
                            "instance_type": instance["InstanceType"],
                            "availability_zone": instance[
                                "Placement"
                            ]["AvailabilityZone"],
                            "private_ip": instance.get(
                                "PrivateIpAddress",
                                "",
                            ),
                            "public_ip": instance.get(
                                "PublicIpAddress",
                                "",
                            ),
                            "vpc_id": instance.get("VpcId", ""),
                            "subnet_id": instance.get(
                                "SubnetId",
                                "",
                            ),
                        }
                    )

    return instances