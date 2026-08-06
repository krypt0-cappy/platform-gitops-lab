from pathlib import Path
from typing import Any

from atlas.aws.inventory.ec2 import collect_instances
from atlas.aws.regions import get_enabled_regions
from atlas.aws.session import get_session
from atlas.reporting.csv_report import write_csv

EC2_FIELDNAMES = [
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


def print_ec2_inventory(
    instances: list[dict[str, Any]],
) -> None:
    print()
    print("Atlas EC2 Inventory")
    print("-" * 120)

    if not instances:
        print("No EC2 instances found.")
        print()
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
    print()


def run_ec2_inventory() -> None:
    session = get_session()
    regions = get_enabled_regions(session)

    instances = collect_instances(
        session=session,
        regions=regions,
    )

    print_ec2_inventory(instances)

    project_root = Path(__file__).resolve().parents[2]
    report_path = project_root / "reports" / "ec2_inventory.csv"

    write_csv(
        rows=instances,
        fieldnames=EC2_FIELDNAMES,
        output_path=report_path,
    )


def run_inventory(arguments: list[str]) -> None:
    if not arguments:
        print("ERROR: Specify an inventory resource.")
        print()
        print("Usage:")
        print("  atlas inventory ec2")
        raise SystemExit(1)

    resource = arguments[0]

    if resource == "ec2":
        run_ec2_inventory()
        return

    print(f"ERROR: Unknown inventory resource: {resource}")
    print()
    print("Supported resources:")
    print("  ec2")
    raise SystemExit(1)
