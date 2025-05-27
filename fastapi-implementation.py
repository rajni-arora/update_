# Check file exists (your existing check is fine)
file_list = s3.list_objects(s3_path)
full_file_path = os.path.join(s3_path, filename)
if full_file_path not in file_list:
    raise HTTPException(404, f"File {filename} not found in {matched_folder}")

# Download only the single file
local_dir = config["paths"].get(f"input_directory_{matched_folder}", f"assets/{matched_folder}/")
os.makedirs(local_dir, exist_ok=True)
local_file_path = os.path.join(local_dir, filename)
s3.download_file(full_file_path, local_file_path)
logger.info(f"Downloaded {matched_folder} file: {filename}")

# Process the single file
preprocessing_main()
logger.info("Preprocessing completed")

# Mark file as processed
processed_files.append(filename)
with open(processed_files_path, 'w') as f:
    json.dump(processed_files, f)

# Archive ONLY the processed file, NOT whole folder
archive_paths = {
    "meta": config['s3_file_paths']['archive_data_path_meta'],
    "knowledge": config['s3_file_paths']['archive_data_path_knowledge']
}
input_path = folders_to_check[matched_folder]
archive_path = archive_paths[matched_folder]

# Pass the single file (full key) to move_objects_with_timestamp
s3.move_objects_with_timestamp(input_path, archive_path, [filename])
logger.info(f"Archived {matched_folder} file: {filename}")