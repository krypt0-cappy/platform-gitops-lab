import sys

from botocore.exceptions import (
    BotoCoreError,
    ClientError,
    NoCredentialsError,
)

from atlas.aws.identity import get_identity
from atlas.aws.regions import get_all_regions
from atlas.aws.session import get_session


def main() -> None:
    session = get_session()
    profile = session.profile_name or "default"
    configured_region = session.region_name or "not configured"

    try:
        identity = get_identity(session)
        regions = get_all_regions(session)

    except NoCredentialsError:
        print(f"ERROR: No credentials found " f"for profile '{profile}'.")
        sys.exit(1)

    except (ClientError, BotoCoreError) as error:
        print(f"ERROR: Unable to query AWS: {error}")
        sys.exit(1)

    print()
    print("####### Atlas AWS Region Inventory #######")
    print("##########################################")
    print(f"Profile              : {profile}")
    print(f"Configured Region    : {configured_region}")
    print(f"Account              : {identity['Account']}")
    print(f"Regions Discovered   : {len(regions)}")
    print("##########################################")
    print()

    for region in regions:
        region_name = region["RegionName"]
        status = region.get("OptInStatus", "unknown")

        print(f"{region_name:<20} {status}")

    print()


if __name__ == "__main__":
    main()
