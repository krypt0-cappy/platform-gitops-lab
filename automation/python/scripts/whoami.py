import sys

from botocore.exceptions import (
    BotoCoreError,
    ClientError,
    NoCredentialsError,
)

from atlas.aws.identity import get_identity
from atlas.aws.session import get_session


def main() -> None:
    session = get_session()
    profile = session.profile_name or "default"
    region = session.region_name or "not configured"

    try:
        identity = get_identity(session)

    except NoCredentialsError:
        print(
            f"ERROR: No AWS credentials found "
            f"for profile '{profile}'."
        )
        sys.exit(1)

    except (ClientError, BotoCoreError) as error:
        print(f"ERROR: Unable to query AWS identity: {error}")
        sys.exit(1)

    print()
    print("Atlas AWS Identity")
    print("------------------------------")
    print(f"Profile : {profile}")
    print(f"Region  : {region}")
    print(f"Account : {identity['Account']}")
    print(f"ARN     : {identity['Arn']}")
    print(f"User ID : {identity['UserId']}")
    print("------------------------------")
    print()


if __name__ == "__main__":
    main()