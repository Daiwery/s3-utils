from .core import get_s3


def list_buckets(args):
    s3 = get_s3(args.profile)
    buckets = s3.list_buckets()["Buckets"]
    for bucket in buckets:
        print(bucket["Name"])
