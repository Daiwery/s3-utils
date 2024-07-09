import boto3


def get_s3(profile):
    session = boto3.session.Session(profile_name=profile)
    s3 = session.client(
        service_name="s3",
        endpoint_url="https://storage.yandexcloud.net",
        region_name="ru-central1",
    )
    return s3


def get_bucket(s3, bucket):
    if bucket == "":
        buckets = s3.list_buckets()["Buckets"]
        if len(buckets) == 0:
            raise ValueError("Count of buckets is equal 0.")
        bucket = buckets[0]["Name"]
    return bucket


