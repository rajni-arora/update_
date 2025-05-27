## Theoretical Flow Explanation

### **Current State (Your Original Code):**
- **Input**: API call triggers download of ALL files from S3 directories
- **Process**: Downloads entire directories (meta, # Add these imports at the top of your api.py file
import json
import os
from fastapi import HTTPException

# Add this new endpoint BEFORE your existing /process-data/ endpoint
@app.post("/process-single-file/")
async def process_single_file(filename: str, file_type: str = "meta"):
    try:
        # Load config
        logger.info("Configuration Loading")
        config = DataProcessor().load_config("configs/config.yml")
        logger.info("Config loaded successfully")
        
        # Check if file already processed
        processed_files_path = os.path.join(config['paths']['output'], 'processed_files.json')
        processed_files = []
        if os.path.exists(processed_files_path):
            with open(processed_files_path, 'r') as f:
                processed_files = json.load(f)
        
        if filename in processed_files:
            raise HTTPException(status_code=400, detail=f"File {filename} is already processed")
        
        # Initialize S3
        logger.info("Read the path, now loading s3 credentials")
        s3 = S3Utils(config['s3_details'])
        
        # Determine S3 path and local directory based on file_type
        if file_type == "meta":
            s3_path = config['s3_file_paths']['input_data_path_meta']
            local_dir = config["paths"].get("input_directory_meta", "assets/meta/")
            s3_file_key = f"{s3_path.rstrip('/')}/{filename}"
        elif file_type == "values":
            s3_path = config['s3_file_paths']['input_data_path_values']  
            local_dir = config["paths"].get("input_directory_values", "assets/values/")
            s3_file_key = f"{s3_path.rstrip('/')}/{filename}"
        elif file_type == "few_shot":
            s3_path = config['s3_file_paths']['few_shot_path']
            local_dir = config["paths"].get("input_directory_few_shot", "assets/few_shot/")
            s3_file_key = f"{s3_path.rstrip('/')}/{filename}"
        else:
            raise HTTPException(status_code=400, detail="Invalid file_type. Use: meta, values, or few_shot")
        
        # Check if file exists in S3
        logger.info(f"Checking if file {filename} exists in S3")
        try:
            # Try to get object metadata to check if file exists
            s3.s3_client.head_object(Bucket=s3.bucket_name, Key=s3_file_key)
            logger.info(f"File {filename} found in S3")
        except:
            raise HTTPException(status_code=404, detail=f"File {filename} not found in S3")
        
        # Create local directory
        os.makedirs(local_dir, exist_ok=True)
        logger.info(f"Created directory {local_dir}")
        
        # Download single file
        local_file_path = os.path.join(local_dir, filename)
        logger.info(f"Downloading {filename}")
        s3.download_file(s3_file_key, local_file_path)
        logger.info(f"File {filename} downloaded successfully")
        
        # Process the file (call your existing preprocessing)
        logger.info("Starting preprocessing main")
        preprocessing_main()
        logger.info("Preprocessing got completed")
        
        # Mark file as processed
        processed_files.append(filename)
        with open(processed_files_path, 'w') as f:
            json.dump(processed_files, f)
        logger.info(f"File {filename} marked as processed")
        
        # Archive the processed file (keeping your existing archive logic)
        if file_type == "meta":
            s3_archive_folder = config['s3_file_paths']['archive_data_path_meta']
            s3.move_objects_with_timestamp(s3_path, s3_archive_folder)
            logger.info("Moved meta file to archive")
        elif file_type == "values":
            s3_archive_folder = config['s3_file_paths']['archive_data_path_values']
            s3.move_objects_with_timestamp(s3_path, s3_archive_folder)
            logger.info("Moved values file to archive")
        # Note: few_shot files are not archived in your original code, so keeping it same
        
        return {
            "status": "success",
            "message": f"File {filename} processed successfully",
            "file": filename,
            "type": file_type
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing file {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


# REPLACE your existing process_data() function with this modified version:
@app.post("/process-data/")
async def process_data():
    try:
        # Load config
        logger.info("Configuration Loading")
        config = DataProcessor().load_config("configs/config.yml")
        logger.info("Config loaded successfully")

        # Input for meta
        logger.info("Reading input_path_meta")
        input_path_meta = config['s3_file_paths']['input_data_path_meta']
        logger.info("Read the path, now loading s3 credentials")
        s3 = S3Utils(config['s3_details'])
        logger.info("Listing file object in input_path_meta")
        file_list = s3.list_objects(input_path_meta)
        
        if not file_list:
            raise HTTPException(status_code=404, detail="No files found to process")
        
        # Process only the FIRST file in the list
        first_file = file_list[0]
        filename = os.path.basename(first_file)
        
        # Check if file already processed
        processed_files_path = os.path.join(config['paths']['output'], 'processed_files.json')
        processed_files = []
        if os.path.exists(processed_files_path):
            with open(processed_files_path, 'r') as f:
                processed_files = json.load(f)
        
        if filename in processed_files:
            raise HTTPException(status_code=400, detail=f"File {filename} is already processed")
        
        logger.info(f"Processing single file: {filename}")
        input_directory_meta = config["paths"].get("input_directory_meta", "assets/meta/")
        os.makedirs(input_directory_meta, exist_ok=True)
        logger.info("Created files_meta")
        files_meta = []
        logger.info("Started the for loop in meta")
        
        # Download only the first file
        download_path = os.path.join(input_directory_meta, filename)
        print("download_path___________", download_path)
        s3.download_file(first_file, download_path)
        files_meta.append(download_path)

        # Continue with rest of your existing logic for few_shot and values...
        # (Keep the existing few_shot and values processing as is)
        
        # Input for few_shot
        logger.info("input_path_few_shot")
        input_path_few_shot = config['s3_file_paths']['few_shot_path']
        logger.info("S3 details for fewshot")
        s3 = S3Utils(config['s3_details'])
        logger.info("file_list for fewshot")
        file_list = s3.list_objects(input_path_few_shot)
        logger.info("Input directory for few shot")
        input_directory_few_Shot = config["paths"].get("input_directory_few_Shot", "assets/few_shot/")
        os.makedirs(input_directory_few_Shot, exist_ok=True)
        logger.info("Empty files_few_Shot list")
        files_few_shot = []
        logger.info("for loop for few_shot")
        for file in file_list:
            download_path = os.path.join(input_directory_few_Shot, os.path.basename(file))
            s3.download_file(file, download_path)
            files_few_shot.append(download_path)

        logger.info("For loop for values")
        for file in file_list:
            download_path = os.path.join(input_directory_values, os.path.basename(file))
            s3.download_file(file, download_path)
            files_values.append(download_path)

        logger.info("s3_knowledge_path initialization")
        s3_knowledge_path = config['s3_file_paths']['knowledge_base_path']
        logger.info("kb_dir path here")
        kb_dir = config['paths']['kb_directory']
        os.makedirs(kb_dir, exist_ok=True)
        logger.info("knowledge_file_name")
        knowledge_file_name = os.path.basename(s3_knowledge_path)
        logger.info("Download files from s3 to local")
        s3.download_file(s3_knowledge_path, kb_dir + knowledge_file_name)

        logger.info("Starting preprocessing main")
        preprocessing_main()
        logger.info("Preprocessing got completed")

        # Mark file as processed
        processed_files.append(filename)
        with open(processed_files_path, 'w') as f:
            json.dump(processed_files, f)
        logger.info(f"File {filename} marked as processed")

        # Archive meta
        s3_archive_folder_meta = config['s3_file_paths']['archive_data_path_meta']
        s3.move_objects_with_timestamp(input_path_meta, s3_archive_folder_meta)
        logger.info("Moved meta")

        # Archive values  
        s3_archive_folder_values = config['s3_file_paths']['archive_data_path_values']
        s3.move_objects_with_timestamp(input_path_values, s3_archive_folder_values)
        logger.info("Moved values")

        return {
            "status": "success", 
            "message": f"Single file {filename} processed successfully",
            "processed_file": filename
        }

    except Exception as e:
        logger.error(f"Error in process_data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))values, few_shot, knowledge_base)
- **Output**: Processes all files at once, then archives everything

### **Modified Approach (What I Proposed):**

## **Forward Flow:**

### **Step 1: API Request**
- **Input**: API call with specific filename and file_type
- **Action**: Instead of "process everything", now it's "process this specific file"

### **Step 2: Validation Check**
- **Input**: Filename from API request
- **Action**: Check two things:
  1. Does this file exist in S3? (HEAD request to S3)
  2. Has this file been processed before? (Check local processed_files.json)
- **Decision Point**: If file doesn't exist OR already processed → throw error and stop

### **Step 3: Single File Download**
- **Input**: Validated filename
- **Action**: Download ONLY that specific file from S3 to local directory
- **Output**: One file in local storage instead of entire directory

### **Step 4: Processing**
- **Input**: Single downloaded file
- **Action**: Run your existing preprocessing_main() function
- **Output**: Processed/indexed data

### **Step 5: Tracking & Archiving**
- **Input**: Successfully processed file
- **Action**: 
  1. Add filename to processed_files.json (so we don't process it again)
  2. Move file from S3 active folder to archive folder (your existing logic)
- **Output**: File marked as "done" and archived

## **What Changes in Information Flow:**

### **Before (Batch Processing):**
```
API Call → Download ALL → Process ALL → Archive ALL → Done
```

### **After (Single File Processing):**
```
API Call (with filename) → Check if valid → Download ONE → Process ONE → Archive ONE → Done
```

## **Backward Flow (Error Handling):**

### **If File Not Found in S3:**
- **Trigger**: S3 HEAD request fails
- **Response**: HTTP 404 error "File not found in S3"
- **Action**: Stop processing, don't download anything

### **If File Already Processed:**
- **Trigger**: Filename exists in processed_files.json
- **Response**: HTTP 400 error "File already processed"
- **Action**: Stop processing, prevent reprocessing

### **If Processing Fails:**
- **Trigger**: preprocessing_main() throws exception
- **Response**: HTTP 500 error with details
- **Action**: File stays in active folder (not archived), can be retried

## **Key Theoretical Benefits:**

1. **Granular Control**: Process files one by one instead of bulk
2. **Error Isolation**: If one file fails, others aren't affected
3. **Restart Capability**: Can resume from where you left off
4. **Resource Management**: Lower memory usage (one file vs entire directory)
5. **Duplicate Prevention**: Won't reprocess same file twice

## **Input/Output Summary:**

**Input**: 
- Filename (string)
- File type (meta/values/few_shot)

**Output**: 
- Success: "File processed and archived"
- Error: Specific error message (not found/already processed/processing failed)

**State Change**: 
- File moves from "S3 active folder" → "Local processing" → "S3 archive folder"
- Filename gets added to "processed files list"

The core concept is changing from "batch processing everything at once" to "controlled single-file processing with state tracking."​​​​​​​​​​​​​​​​