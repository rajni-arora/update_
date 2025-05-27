from fastapi import FastAPI, HTTPException, Request
import os, json, logging
from utils.s3_utils import S3Utils
from utils.data_processor import DataProcessor
from preprocessing import preprocessing_main

app = FastAPI()
logger = logging.getLogger("uvicorn")

@app.post("/process-data/")
async def process_data(request: Request):
    try:
        # Load config
        logger.info("Loading config")
        config = DataProcessor().load_config("configs/config.yml")

        # Get filename from request body
        body = await request.json()
        filename = body.get("filename")
        if not filename:
            raise HTTPException(status_code=400, detail="Filename is required in the request body")

        # S3 setup
        s3 = S3Utils(config['s3_details'])

        # Define the folders to check
        folders_to_check = {
            "meta": config['s3_file_paths']['input_data_path_meta'],
            "knowledge": config['s3_file_paths']['input_data_path_kb']
        }

        # Check file existence in both folders
        for folder_name, s3_path in folders_to_check.items():
            file_list = s3.list_objects(s3_path)
            full_file_path = os.path.join(s3_path, filename)
            if full_file_path not in file_list:
                raise HTTPException(
                    status_code=404,
                    detail=f"File '{filename}' not found in S3 '{folder_name}' folder"
                )

        # Check if file already processed
        processed_files_path = os.path.join(config['paths']['output'], 'processed_files.json')
        processed_files = []
        if os.path.exists(processed_files_path):
            with open(processed_files_path, 'r') as f:
                processed_files = json.load(f)

        if filename in processed_files:
            raise HTTPException(status_code=400, detail=f"File {filename} already processed")

        # Download files from both folders
        for folder_name, s3_path in folders_to_check.items():
            local_dir = config["paths"].get(f"input_directory_{folder_name}", f"assets/{folder_name}/")
            os.makedirs(local_dir, exist_ok=True)
            local_file_path = os.path.join(local_dir, filename)
            full_file_path = os.path.join(s3_path, filename)
            s3.download_file(full_file_path, local_file_path)
            logger.info(f"Downloaded {folder_name} file: {filename}")

        # Run preprocessing
        preprocessing_main()
        logger.info("Preprocessing completed")

        # Mark file as processed
        processed_files.append(filename)
        with open(processed_files_path, 'w') as f:
            json.dump(processed_files, f)

        # Archive files from meta and knowledge
        archive_paths = {
            "meta": config['s3_file_paths']['archive_data_path_meta'],
            "knowledge": config['s3_file_paths']['archive_data_path_kb']
        }

        for folder_name in folders_to_check.keys():
            input_path = folders_to_check[folder_name]
            archive_path = archive_paths[folder_name]
            s3.move_objects_with_timestamp(input_path, archive_path, [filename])
            logger.info(f"Archived {folder_name} file: {filename}")

        return {
            "status": "success",
            "message": f"File {filename} processed successfully from both meta and knowledge",
            "processed_file": filename
        }

    except Exception as e:
        logger.error(f"Error in process_data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))