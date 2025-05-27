Looking at your code, I can see you want to modify the preprocessing pipeline to process files one by one instead of processing entire directories. Based on your images, I can see you have a `DataProcessor` class with methods like `load_config`, `create_directories`, and `read_metadata`.

Here's the logic you need to add:

## Key Changes Needed:

### 1. **Add file tracking mechanism**
You'll need to track which files have been processed. Add this to your config or create a separate tracking file.

### 2. **Modify the main processing method**
Instead of processing all files in a directory, process one file at a time based on the API request.

### 3. **Add S3 file existence check**
Before downloading, check if the file exists in S3.

### 4. **Add processed file tracking**
Keep track of processed files to avoid reprocessing.

## Code Changes:

### In your `DataProcessor` class, add these new methods:

```python
import boto3
import json
import os

def check_file_exists_in_s3(self, bucket_name, file_key):
    """Check if file exists in S3 bucket"""
    try:
        s3_client = boto3.client('s3')
        s3_client.head_object(Bucket=bucket_name, Key=file_key)
        return True
    except:
        return False

def load_processed_files(self):
    """Load list of already processed files"""
    processed_file_path = os.path.join(self.config['paths']['output'], 'processed_files.json')
    if os.path.exists(processed_file_path):
        with open(processed_file_path, 'r') as f:
            return json.load(f)
    return []

def save_processed_file(self, filename):
    """Save processed file name to tracking file"""
    processed_files = self.load_processed_files()
    if filename not in processed_files:
        processed_files.append(filename)
        processed_file_path = os.path.join(self.config['paths']['output'], 'processed_files.json')
        with open(processed_file_path, 'w') as f:
            json.dump(processed_files, f)

def download_single_file_from_s3(self, bucket_name, file_key, local_path):
    """Download single file from S3"""
    try:
        s3_client = boto3.client('s3')
        s3_client.download_file(bucket_name, file_key, local_path)
        logger.info(f"Downloaded {file_key} to {local_path}")
        return True
    except Exception as e:
        logger.error(f"Error downloading {file_key}: {str(e)}")
        return False

def process_single_file(self, filename, file_type='metadata'):
    """Process single file instead of entire directory"""
    # Check if file already processed
    processed_files = self.load_processed_files()
    if filename in processed_files:
        raise Exception(f"File {filename} has already been processed")
    
    # Determine S3 path based on file type
    if file_type == 'metadata':
        s3_key = f"meta/{filename}"
        local_dir = self.config['paths']['metadata']
    elif file_type == 'values':
        s3_key = f"values/{filename}"
        local_dir = self.config['paths']['values']
    elif file_type == 'knowledge':
        s3_key = f"knowledge_base_data/{filename}"
        local_dir = self.config['paths']['kb_directory']
    else:
        raise Exception(f"Unknown file type: {file_type}")
    
    # Check if file exists in S3
    bucket_name = "your-s3-bucket-name"  # Replace with your actual bucket name
    if not self.check_file_exists_in_s3(bucket_name, s3_key):
        raise Exception(f"File {filename} not found in S3 bucket")
    
    # Download single file
    local_file_path = os.path.join(local_dir, filename)
    if not self.download_single_file_from_s3(bucket_name, s3_key, local_file_path):
        raise Exception(f"Failed to download {filename}")
    
    # Process the single file (your existing processing logic here)
    self.process_file_content(local_file_path, file_type)
    
    # Mark file as processed
    self.save_processed_file(filename)
    
    logger.info(f"Successfully processed {filename}")
    return True
```

### Replace your existing batch processing method with:

**REPLACE THIS** (in your existing code where you process entire directories):
```python
# Your current directory processing logic
for filekey in os.listdir(meta_path):
    # process all files
```

**WITH THIS**:
```python
def process_request(self, filename, file_type='metadata'):
    """Main method called by API to process single file"""
    try:
        # Create directories if needed
        self.create_directories()
        
        # Process single file
        result = self.process_single_file(filename, file_type)
        
        return {
            "status": "success",
            "message": f"File {filename} processed successfully",
            "file": filename
        }
    except Exception as e:
        logger.error(f"Error processing {filename}: {str(e)}")
        return {
            "status": "error",
            "message": str(e),
            "file": filename
        }
```

### Update your API endpoint to call the new method:

**REPLACE** your current API endpoint that processes entire directories:
```python
# Your current API call
processor.read_metadata()  # or similar method
```

**WITH**:
```python
# New API call for single file
result = processor.process_request(filename="your_file.json", file_type="metadata")
```

### Add to your config.yml:
```yaml
s3:
  bucket_name: "your-bucket-name"
  region: "your-region"
```

## Summary of Changes:

1. **Line replacements**: Replace your batch directory processing with single file processing
2. **New methods added**: 5 new methods for S3 checking, file tracking, and single file processing
3. **API modification**: Change your API endpoint to accept filename parameter
4. **Config update**: Add S3 configuration

This approach ensures that:
- Only one file is processed per API call
- Files are checked for existence in S3 before downloading
- Already processed files are tracked and skipped
- Each file is fully processed before moving to the next one

Would you like me to help you implement any specific part of this logic in more detail?​​​​​​​​​​​​​​​​