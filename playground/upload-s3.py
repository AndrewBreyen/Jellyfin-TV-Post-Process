import os
import boto3

def upload_to_s3(file_path, bucket_name):
    """Upload a file to an S3 bucket."""
    # Extract file name from file path
    object_name = os.path.basename(file_path)

    # Create S3 client
    s3_client = boto3.client('s3')

    # Uploads the given file using a managed uploader, which will split up large
    # files automatically and upload parts in parallel.
    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
    except Exception as e:
        print(f"Error uploading file {file_path} to bucket {bucket_name}: {e}")
        return False
    else:
        print(f"File uploaded successfully to S3 bucket {bucket_name} with key {object_name}")
        return True

# Example usage:
file_path = 'sample.log'  # Replace with your file path
bucket_name = 'jellyfin-tv-postprocess'  # Replace with your bucket name
upload_to_s3(file_path, bucket_name)
