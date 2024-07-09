import sys
import threading
import os
from .core import get_s3, get_bucket


class ProgressUploadPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            s = "\r%s  %s / %s  (%.2f%%)" % (
                self._filename, self._seen_so_far, int(self._size), percentage
            )
            sys.stdout.write(s)
            sys.stdout.flush()


def upload(args):
    if os.path.basename(args.key) != "" and len(args.path) > 1:
        raise ValueError(
            "Key doesn't like a dir-path, but the count of files is not equal 1."
        )

    keys = []
    if os.path.basename(args.key) == "":
        for path in args.path:
            keys.append(os.path.join(args.key, os.path.basename(path)))
    else:
        keys = [args.key]

    s3 = get_s3(args.profile)
    args.bucket = get_bucket(s3, args.bucket)

    for i, path in enumerate(args.path):
        s3.upload_file(
            path, args.bucket, keys[i],
            Callback=ProgressUploadPercentage(path)
        )
        print()
