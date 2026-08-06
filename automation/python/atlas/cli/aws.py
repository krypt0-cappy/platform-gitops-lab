from atlas.aws.identity import get_identity
from atlas.aws.regions import get_all_regions
from atlas.aws.session import get_session


def run_whoami() -> None:
    session = get_session()
    identity = get_identity(session)

    print()
    print("Atlas AWS Identity")
    print("------------------------------")
    print(f"Profile : {session.profile_name or 'default'}")
    print(f"Region  : {session.region_name or 'not configured'}")
    print(f"Account : {identity['Account']}")
    print(f"ARN     : {identity['Arn']}")
    print(f"User ID : {identity['UserId']}")
    print()


def run_regions() -> None:
    session = get_session()
    regions = get_all_regions(session)

    print()
    print("Atlas AWS Regions")
    print("------------------------------")

    for region in regions:
        print(f"{region['RegionName']:<20}" f"{region.get('OptInStatus', 'unknown')}")

    print()
