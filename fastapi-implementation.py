import os
from datetime import datetime

async def data_ingestion():
    app_env = "e1"
    config_path = f'configs/config_{app_env}.yml'
    print(config_path)

    # Load config
    logger.info("Configuration Loading")
    config = DataProcessor().load_config(config_path)
    secrets_to_env(config)
    logger.info("Config loaded successfully")

    s3 = S3Utils(config['s3_details'])

    # Get current timestamp for file naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    local_assets_path = "assets/"
    s3_assets_path = config['s3_file_paths']['s3_assets_upload_path']
    s3_archive_path = config['s3_file_paths']['archive_data_path']

    # Folders where timestamp should be added
    timestamped_folders = {"meta", "values", "knowledge"}

    for root, dirs, files in os.walk(local_assets_path):
        for file in files:
            local_file_path = os.path.join(root, file).replace("\\", "/")
            relative_path = local_file_path.replace(local_assets_path, "")
            folder_name = relative_path.split('/')[0]

            # Construct S3 key
            if folder_name in timestamped_folders:
                file_name, file_ext = os.path.splitext(os.path.basename(file))
                timestamped_filename = f"{file_name}_{timestamp}{file_ext}"
                folder_path = os.path.dirname(relative_path)
                s3_archive_key = f"{s3_archive_path}/{folder_path}/{timestamped_filename}"
            else:
                # Upload as-is for non-timestamp folders (like 'others')
                s3_archive_key = f"{s3_archive_path}/{relative_path}"

            print(f"Archiving: {s3_archive_key}")
            s3.upload_file(local_file_path, s3_archive_key)