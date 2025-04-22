# Output folder path
s3_output_folder = config['s3_file_paths']['output_data_path']
output_folder = os.path.abspath(config['paths']['output'])
output_files = os.listdir(output_folder)

for output_file in output_files:
    file_path = os.path.join(output_folder, output_file)

    if os.path.isfile(file_path):
        with open(file_path, "rb") as f:
            file_name = os.path.basename(file_path)
            logger.info(f"Uploading {file_name} from {file_path} to S3...")

            identifiers = {
                "project_type": "Gleam",
                "folder_state": "Active",
                "use_case": "indexing"
            }

            try:
                s3.upload_file_without_creds(f, file_name, identifiers)
                logger.info(f"File uploaded successfully: {file_name}")
            except Exception as e:
                logger.error(f"Failed to upload {file_name}: {str(e)}")
    else:
        logger.warning(f"Skipped non-file entry: {file_path}")