import os

# ... (rest of your existing code)

if response_indexing.status_code != 200:
    raise Exception(status_code=response_indexing.status_code, detail=response_indexing.json())
else:
    logger.info(f"Indexing successful. Response:\n{response_indexing.json()}")
    
    # Delete the file after successful indexing
    try:
        os.remove(file_path)
        logger.info(f"Deleted file after successful indexing: {file_path}")
    except Exception as e:
        logger.error(f"Failed to delete file ({file_path}): {e}")
    
    # Delete all files in the output directory
    try:
        output_dir = os.path.dirname(file_path)
        for file in os.listdir(output_dir):
            full_path = os.path.join(output_dir, file)
            if os.path.isfile(full_path):
                os.remove(full_path)
                logger.info(f"Deleted file: {full_path}")
    except Exception as e:
        logger.error(f"Failed to delete files in directory {output_dir}: {e}")