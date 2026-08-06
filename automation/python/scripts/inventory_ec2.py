import sys
from pathlib import Path
from typing import Any

from botocore.exceptions import (
    BotoCoreError,
    ClientError,
    NoCredentialsError,
)

from atlas.aws.inventory.ec2 import collect_instances
from atlas.aws.regions import get_enabled_regions
from atlas.aws.session import get_session
from atlas.reporting.csv_report import write_csv

FIELDNAMES = [
    "region",
    "instance_id",
    "name",
    "state",
    "instance_type",
    "availability_zone",
    "private_ip",
    "public_ip",
    "vpc_id",
    "subnet_id",
]


def print_inventory(
    instances: list[dict[str, Any]],
) -> None:
    print()
    print("Atlas EC2 Inventory")
    print("-" * 120)

    if not instances:
        print("No EC2 instances found.")
        return

    header = (
        f"{'Region':<15}"
        f"{'Instance ID':<22}"
        f"{'Name':<24}"
        f"{'State':<12}"
        f"{'Type':<14}"
        f"{'Availability Zone':<20}"
        f"{'Private IP':<16}"
        f"{'Public IP':<16}"
    )

    print(header)
    print("-" * 120)

    for instance in instances:
        print(
            f"{instance['region']:<15}"
            f"{instance['instance_id']:<22}"
            f"{instance['name']:<24}"
            f"{instance['state']:<12}"
            f"{instance['instance_type']:<14}"
            f"{instance['availability_zone']:<20}"
            f"{instance['private_ip']:<16}"
            f"{instance['public_ip']:<16}"
        )

    print()
    print(f"Total instances: {len(instances)}")


def main() -> None:
    session = get_session()

    output_path = Path(__file__).resolve().parents[1] / "output" / "ec2_inventory.csv"

    try:
        regions = get_enabled_regions(session)
        instances = collect_instances(
            session,
            regions,
        )

    except NoCredentialsError:
        print("ERROR: AWS credentials were not found.")
        sys.exit(1)

    except (ClientError, BotoCoreError) as error:
        print(f"ERROR: Unable to query AWS: {error}")
        sys.exit(1)

    print_inventory(instances)

    write_csv(
        rows=instances,
        fieldnames=FIELDNAMES,
        output_path=output_path,
    )


if __name__ == "__main__":
    main()
