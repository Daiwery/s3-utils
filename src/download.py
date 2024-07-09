from .core import get_s3, get_bucket
from pathlib import Path
import os
from tqdm import tqdm


def download(args):
    # Create session.
    s3 = get_s3(args.profile)
    args.bucket = get_bucket(s3, args.bucket)
    if args.keys == "all":
        args.keys = s3.list_objects(Bucket=args.bucket)["Contents"]
        args.keys = list(map(lambda item: item["Key"], args.keys))

    # Calculate unique directories.
    dirs = []
    for key in args.keys:
        path = Path(key)
        if args.dir != "":
            path = Path(args.dir).joinpath(path)
        for part in path.parents[::-1][1:]:
            if part not in dirs:
                dirs.append(part)

    # Create necessary directories.
    for i_dir in dirs:
        if not os.path.exists(i_dir):
            os.mkdir(i_dir)

    # Download.
    keys = tqdm(args.keys, desc="Download")
    for key in keys:
        keys.set_description(f"Download ({os.path.basename(key)})")
        s3.download_file(args.bucket, key, os.path.join(args.dir, key))
