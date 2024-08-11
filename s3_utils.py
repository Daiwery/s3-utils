import argparse
from src.list_buckets import list_buckets
from src.list_objects import list_objects
from src.upload import upload
from src.download import download
from src.sync import sync


def create_parser():
    parser = argparse.ArgumentParser(
        description="Some utils for working with yandex s3-storage based on the boto3 packaged."
    )
    parser.add_argument("profile", help="The profile from .aws/credentials")

    subparsers = parser.add_subparsers()

    # --------------- list_buckets ---------------
    parser_list_buckets = subparsers.add_parser(
        "buckets", help="Show the list of buckets."
    )
    parser_list_buckets.set_defaults(func=list_buckets)

    # --------------- list_objects ---------------
    parser_list_objects = subparsers.add_parser(
        "objects", help="Show the list of objects in the given bucket."
    )
    parser_list_objects.add_argument(
        "-bucket", default="",
        help="The name of the bucket (default: a first bucket is selected)"
    )
    parser_list_objects.set_defaults(func=list_objects)

    # --------------- upload ---------------
    parser_upload = subparsers.add_parser(
        "upload", help="Upload files into the given bucket."
    )
    parser_upload.add_argument(
        "-bucket", default="",
        help="The name of the bucket (default: a single bucket is selected)"
    )
    parser_upload.add_argument("path", nargs="+", help="Path to file")
    parser_upload.add_argument(
        "key", help="The key (auto add the name of files if key likes a dir-path)"
    )
    parser_upload.add_argument(
        "--rel", action="store_true", 
        help="If it is true save relative dirs in paths"
    )
    parser_upload.set_defaults(func=upload)

    # --------------- download ---------------
    parser_download = subparsers.add_parser(
        "download", help="Download files from the given bucket."
    )
    parser_download.add_argument(
        "-bucket", default="",
        help="The name of the bucket (default: a single bucket is selected)"
    )
    parser_download.add_argument(
        "-dir", default=".",
        help="The parent directory for files (default: current directory)"
    )
    parser_download.add_argument(
        "--basename", action="store_true",
        help="If it is true convert keys to base names."
    )
    parser_download.add_argument(
        "keys", nargs="*", default="all",
        help="The keys of the objects to download (default: all files)"
    )
    parser_download.set_defaults(func=download)

    # --------------- sync ---------------
    parser_sync = subparsers.add_parser(
        "sync", help="Synchronize two dirs. Do changes on the given bucket."
    )
    parser_sync.add_argument(
        "-bucket", default="",
        help="The name of the bucket (default: a single bucket is selected)"
    )
    parser_sync.add_argument(
        "new", help="The path to the new version of the data"
    )
    parser_sync.add_argument(
        "old", help="The path to the old version of the data"
    )
    parser_sync.set_defaults(func=sync)

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
