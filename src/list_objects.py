from .core import get_s3, get_bucket


def list_objects(args):
    s3 = get_s3(args.profile)
    args.bucket = get_bucket(s3, args.bucket)
    for key in s3.list_objects(Bucket=args.bucket)["Contents"]:
        print(key["Key"])
