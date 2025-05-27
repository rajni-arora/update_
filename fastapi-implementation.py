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

        # Get filename from request query or body
        body = await request.json()
        filename = body.get("filename")
        if not filename:
            raise HTTPException(status_code=400, detail="Filename is required in the request body")

        # S3 setup
        s3 = S3Utils(config['s3_details'])

        # Check if file exists in S3
        input_path_meta = config['s3_file_paths']['input_data_path_meta']
        full_file_path = os.path.join(input_path_meta, filename)
        file_list = s3.list_objects(input_path_meta)

        if full_file_path not in file_list:
            raise HTTPException(status_code=404, detail=f"File {filename} not found in S3")

        # Check if file already processed
        processed_files_path = os.path.join(config['paths']['output'], 'processed_files.json')
        processed_files = []
        if os.path.exists(processed_files_path):
            with open(processed_files_path, 'r') as f:
                processed_files = json.load(f)

        if filename in processed_files:
            raise HTTPException(status_code=400, detail=f"File {filename} already processed")

        # Download file
        input_directory_meta = config["paths"].get("input_directory_meta", "assets/meta/")
        os.makedirs(input_directory_meta, exist_ok=True)
        local_file_path = os.path.join(input_directory_meta, filename)
        s3.download_file(full_file_path, local_file_path)
        logger.info(f"Downloaded file: {filename}")

        # (Optional) Handle few_shot, values, and knowledge base as before
        # You can keep existing logic to download those

        # Run preprocessing
        preprocessing_main()
        logger.info("Preprocessing completed")

        # Mark file as processed
        processed_files.append(filename)
        with open(processed_files_path, 'w') as f:
            json.dump(processed_files, f)

        # Archive file
        s3_archive_folder_meta = config['s3_file_paths']['archive_data_path_meta']
        s3.move_objects_with_timestamp(input_path_meta, s3_archive_folder_meta, [filename])
        logger.info(f"Archived file: {filename}")

        return {
            "status": "success",
            "message": f"File {filename} processed successfully",
            "processed_file": filename
        }

    except Exception as e:
        logger.error(f"Error in process_data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))