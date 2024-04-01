import os
import boto3

def download_from_s3(bucket_name, local_directory):
    """Download all files from an S3 bucket to a local directory."""
    # Create S3 client
    s3_client = boto3.client('s3')

    # List all objects in the bucket
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
    except Exception as e:
        print(f"Error listing objects in bucket {bucket_name}: {e}")
        return False

    # Ensure local directory exists
    os.makedirs(local_directory, exist_ok=True)

    # Download each object
    for obj in response.get('Contents', []):
        key = obj['Key']
        local_file_path = os.path.join(local_directory, key)
        try:
            s3_client.download_file(bucket_name, key, local_file_path)
        except Exception as e:
            print(f"Error downloading file {key} from bucket {bucket_name}: {e}")
        else:
            print(f"File downloaded successfully: {local_file_path}")

# Example usage:
bucket_name = 'jellyfin-tv-postprocess'  # Replace with your bucket name
current_directory = os.getcwd()  # Get the current working directory
local_directory = os.path.join(current_directory, 's3-download')  # Create the local directory path
download_from_s3(bucket_name, local_directory)
