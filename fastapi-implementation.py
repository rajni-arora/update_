found = False
for folder_name, s3_path in folders_to_check.items():
    file_list = s3.list_objects(s3_path)
    full_file_path = os.path.join(s3_path, filename)
    if full_file_path in file_list:
        found = True
        matched_folder = folder_name
        matched_path = s3_path
        break

if not found:
    raise HTTPException(
        status_code=404,
        detail=f"File '{filename}' not found in S3 'meta' or 'knowledge' folders"
    )
    
    
    
    
    
    
local_dir = config["paths"].get(f"input_directory_{matched_folder}", f"assets/{matched_folder}/")
os.makedirs(local_dir, exist_ok=True)
local_file_path = os.path.join(local_dir, filename)
full_file_path = os.path.join(matched_path, filename)

s3.download_file(full_file_path, local_file_path)
logger.info(f"Downloaded {matched_folder} file: {filename}")


input_path = folders_to_check[matched_folder]
archive_path = archive_paths[matched_folder]

s3.move_objects_with_timestamp(input_path, archive_path, [filename])
logger.info(f"Archived {matched_folder} file: {filename}")
