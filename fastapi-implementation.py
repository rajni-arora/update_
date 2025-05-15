import os

# ... existing code ...

if response_indexing.status_code != 200:
    raise Exception(status_code=response_indexing.status_code, detail=response_indexing.json())
else:
    logging.info(f"Indexing successful. Response:\n{response_indexing.json()}")
    # Delete the file after successful indexing
    try:
        os.remove(file_path)
        logging.info(f"Deleted file after successful indexing: {file_path}")
    except Exception as e:
        logging.error(f"Failed to delete file {file_path}: {e}")