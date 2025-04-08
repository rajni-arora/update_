from s3_utils import S3Utils  # Assuming this is your shared S3 utility module
import configparser

# Load config file (same config used in your real system)
config = configparser.ConfigParser()
config.read('config.ini')  # or wherever your actual config is

# Instantiate the S3 Utility
s3 = S3Utils(config)

# Set a prefix (folder path in the bucket)
prefix = "your/input/directory/prefix/"  # e.g., "data/assets/"

# Try to list the files in the given S3 path
files = s3.list_objects(prefix)

# Print out the contents
print("Files found in S3 path:")
for f in files:
    print(f)

# Optional: Assert or log if directory is empty
if not files:
    print("No files found or unable to access path.")