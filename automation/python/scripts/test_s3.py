from atlas.aws.inventory.s3 import collect_buckets
from atlas.aws.session import get_session

session = get_session()

buckets = collect_buckets(session)

print()

for bucket in buckets:
    print(bucket)
