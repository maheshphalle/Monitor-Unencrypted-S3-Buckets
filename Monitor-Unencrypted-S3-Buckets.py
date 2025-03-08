import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    s3 = boto3.client("s3")

    try:
        # Get list of all S3 buckets
        response = s3.list_buckets()
    except ClientError as e:
        print(f"Error listing buckets: {e}")
        return {"error": str(e)}

    unencrypted_buckets = []

    for bucket in response.get("Buckets", []):
        bucket_name = bucket["Name"]

        try:
            # Check if bucket has server-side encryption enabled
            s3.get_bucket_encryption(Bucket=bucket_name)
        except ClientError as e:
            if e.response["Error"]["Code"] == "ServerSideEncryptionConfigurationNotFoundError":
                unencrypted_buckets.append(bucket_name)

    # Log unencrypted buckets
    if unencrypted_buckets:
        print(f"Unencrypted S3 Buckets Found: {unencrypted_buckets}")
    else:
        print("All buckets have encryption enabled.")

    return {"unencrypted_buckets": unencrypted_buckets}
