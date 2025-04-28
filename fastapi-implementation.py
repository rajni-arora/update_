Looking at your code, I can see you're implementing an archiving functionality using S3 to move objects from an input path to archive folders. You want to add a timestamp to the files before moving them to the target folders.

Here's how we can add a timestamp to the files before moving them:

Old lines:
```python
#Archive meta
s3_archive_folder_meta = config['s3_file_paths']['archive_data_path_meta']
s3.move_objects(input_path_meta, s3_archive_folder_meta)

#Archive values
s3_archive_folder_values = config['s3_file_paths']['archive_data_path_values']
s3.move_objects(input_path_values, s3_archive_folder_values)

#Archive Knowledge
s3_archive_folder_knowledge = config['s3_file_paths']['archive_data_path_Knowledge']
s3.move_objects(s3_knowledge_path, s3_archive_folder_knowledge)

#Archive Others/miscellineous
s3_archive_folder_few_shot = config['s3_file_paths']['archive_data_path_Others']
s3.move_objects(input_path_few_shot, s3_archive_folder_few_shot)
```

New lines:
```python
# Generate timestamp for archiving
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

#Archive meta
s3_archive_folder_meta = config['s3_file_paths']['archive_data_path_meta']
s3.move_objects(input_path_meta, f"{s3_archive_folder_meta}/{timestamp}")

#Archive values
s3_archive_folder_values = config['s3_file_paths']['archive_data_path_values']
s3.move_objects(input_path_values, f"{s3_archive_folder_values}/{timestamp}")

#Archive Knowledge
s3_archive_folder_knowledge = config['s3_file_paths']['archive_data_path_Knowledge']
s3.move_objects(s3_knowledge_path, f"{s3_archive_folder_knowledge}/{timestamp}")

#Archive Others/miscellineous
s3_archive_folder_few_shot = config['s3_file_paths']['archive_data_path_Others']
s3.move_objects(input_path_few_shot, f"{s3_archive_folder_few_shot}/{timestamp}")
```

This change:
1. Adds an import for datetime at the beginning of the relevant section
2. Creates a timestamp variable in the format "YYYYMMDD_HHMMSS"
3. Modifies each target path to include the timestamp as a subfolder, which effectively groups files archived at the same time together

The timestamp format matches what's shown in your terminal output for the schema and knowledge data files.​​​​​​​​​​​​​​​​