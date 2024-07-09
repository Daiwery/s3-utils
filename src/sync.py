from .core import get_s3, get_bucket
from pathlib import Path
import os
import filecmp
from tqdm import tqdm
import mimetypes


def sync(args):
    args.new = os.path.abspath(args.new)
    args.old = os.path.abspath(args.old)

    # Calculate plan.
    new_files = set([
        path.relative_to(args.new) for path in Path(args.new).rglob("*") if path.is_file()
    ])
    old_files = set([
        path.relative_to(args.old) for path in Path(args.old).rglob("*") if path.is_file()
    ])

    intersection = old_files & new_files
    to_delete = old_files - new_files
    to_upload = new_files - old_files
    changed = []
    for key in intersection:
        if not filecmp.cmp(Path(args.old).joinpath(key), Path(args.new).joinpath(key)):
            changed.append(key)

    print(f"{len(to_delete)} files to delete")
    print(f"{len(to_upload)} new files")
    print(f"{len(changed)} files from {len(intersection)} are changed")
    to_upload |= set(changed)
    print(f"{len(to_upload)} files to upload")

    # Do.
    s3 = get_s3(args.profile)
    args.bucket = get_bucket(s3, args.bucket)

    to_delete = tqdm(to_delete, desc="Delete")
    for key in to_delete:
        to_delete.set_description(f"Delete ({key})")
        s3.delete_object(Bucket=args.bucket, Key=str(key))

    to_upload = tqdm(to_upload, desc="Upload")
    for key in to_upload:
        to_upload.set_description(f"Upload ({key})")

        path = Path(args.new).joinpath(key)
        content_type = mimetypes.guess_type(str(key))[0]

        ExtraArgs = None
        if content_type is not None:
            ExtraArgs = {"ContentType": content_type}

        s3.upload_file(
            path, args.bucket, str(key),
            ExtraArgs=ExtraArgs
        )

    os.system(f"rm -r {args.old}")
    os.system(f"cp -r {args.new} {args.old}")
    print("Delete and copy!")
