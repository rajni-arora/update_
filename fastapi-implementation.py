import os
from pathlib import Path

def upload_all_files_to_s3(s3, source_dir_path, destination_dir_path):
    """
    Upload all files from local source_dir_path to S3 destination_dir_path.

    :param s3: An instance of the S3Utils class with the upload_file method.
    :param source_dir_path: Local path to the directory containing files to upload.
    :param destination_dir_path: Destination path in S3 where files should be uploaded.
    """
    source_dir = Path(source_dir_path)
    destination_dir = Path(destination_dir_path)

    # Check if source_dir exists
    if not source_dir.exists() or not source_dir.is_dir():
        raise ValueError(f"Source directory '{source_dir}' does not exist or is not a directory.")

    for file_path in source_dir.iterdir():
        if file_path.is_file():
            destination_path = destination_dir / file_path.name
            print(f"Uploading {file_path} to {destination_path}")
            s3.upload_file(str(file_path), str(destination_path))