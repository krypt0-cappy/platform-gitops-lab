from atlas.aws.inventory.s3 import (
    get_bucket_region,
    get_encryption_status,
    get_public_access_block_status,
    get_versioning_status,
)


class FakeS3Client:
    def __init__(
        self,
        *,
        location=None,
        versioning=None,
        encryption=None,
        public_access_block=None,
    ):
        self.location = location
        self.versioning = versioning or {}
        self.encryption = encryption or {}
        self.public_access_block = public_access_block or {}

    def get_bucket_location(self, Bucket: str):
        return {
            "LocationConstraint": self.location,
        }

    def get_bucket_versioning(self, Bucket: str):
        return self.versioning

    def get_bucket_encryption(self, Bucket: str):
        return self.encryption

    def get_public_access_block(self, Bucket: str):
        return {
            "PublicAccessBlockConfiguration": self.public_access_block,
        }


def test_get_bucket_region_defaults_to_us_east_1() -> None:
    s3 = FakeS3Client(location=None)

    assert get_bucket_region(s3, "test-bucket") == "us-east-1"


def test_get_bucket_region_returns_region() -> None:
    s3 = FakeS3Client(location="us-west-2")

    assert get_bucket_region(s3, "test-bucket") == "us-west-2"


def test_get_versioning_status_enabled() -> None:
    s3 = FakeS3Client(
        versioning={
            "Status": "Enabled",
        }
    )

    assert get_versioning_status(s3, "test-bucket") == "Enabled"


def test_get_versioning_status_defaults_to_disabled() -> None:
    s3 = FakeS3Client()

    assert get_versioning_status(s3, "test-bucket") == "Disabled"


def test_get_encryption_status_returns_algorithm() -> None:
    s3 = FakeS3Client(
        encryption={
            "ServerSideEncryptionConfiguration": {
                "Rules": [
                    {
                        "ApplyServerSideEncryptionByDefault": {
                            "SSEAlgorithm": "AES256",
                        }
                    }
                ]
            }
        }
    )

    assert get_encryption_status(s3, "test-bucket") == "AES256"


def test_public_access_block_fully_blocked() -> None:
    s3 = FakeS3Client(
        public_access_block={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True,
        }
    )

    assert (
        get_public_access_block_status(
            s3,
            "test-bucket",
        )
        == "Fully blocked"
    )
