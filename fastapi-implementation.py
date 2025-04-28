from datetime import datetime
import os

# Example for values
input_path_values = config['s3_file_paths']['input_path_values']
bucket_values = input_path_values.split('/')[0]
prefix_values = '/'.join(input_path_values.split('/')[1:])

# Generate timestamp
timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')

# Create a new destination folder path with timestamped file
s3_archive_folder_values = config['s3_file_paths']['archive_data_path_values']

# Add timestamp suffix to the folder (not modifying the move_objects function)
s3_archive_folder_values_with_timestamp = os.path.join(
    s3_archive_folder_values.rstrip('/'),
    timestamp
)

# Then call move_objects as usual
s3.move_objects(input_path_values, s3_archive_folder_values_with_timestamp)