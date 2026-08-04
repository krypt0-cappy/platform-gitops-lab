import boto3


def main():

    sts = boto3.client("sts")

    identity = sts.get_caller_identity()

    print()

    print("AWS Identity")
    print("------------------------")
    print(f"Account : {identity['Account']}")
    print(f"User ARN: {identity['Arn']}")
    print(f"User ID : {identity['UserId']}")


if __name__ == "__main__":
    main()

