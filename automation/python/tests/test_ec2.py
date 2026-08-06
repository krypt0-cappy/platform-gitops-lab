from atlas.aws.inventory.ec2 import get_name_tag


def test_get_name_tag_returns_name() -> None:
    tags = [
        {"Key": "Environment", "Value": "dev"},
        {"Key": "Name", "Value": "atlas-server"},
    ]

    assert get_name_tag(tags) == "atlas-server"


def test_get_name_tag_returns_empty_string_without_name() -> None:
    tags = [
        {"Key": "Environment", "Value": "dev"},
    ]

    assert get_name_tag(tags) == ""


def test_get_name_tag_returns_empty_string_without_tags() -> None:
    assert get_name_tag(None) == ""