output_folder = os.path.abspath(config['paths']['output'])  # Local folder path
output_files = os.listdir(output_folder)  # List of files in output folder

for output_file in output_files:
    file_path = os.path.join(output_folder, output_file)  # Full file path
    file_name = os.path.basename(output_file)

    with open(file_path, "rb") as f:
        logger.info(f"Uploading {file_name} to S3...")
        
        identifiers = {
            "project_type": "Gleam",
            "folder_state": "Active",
            "use_case": "indexing"
        }

        # Make sure you are passing the file object here!
        s3.upload_file_without_creds(f, file_name, identifiers)
        
        
        
        
        
        
        def upload_file_without_creds(self, file, file_name, identifiers):
    okta_token = self._get_okta_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"claims impersonation_id={os.getenv('AIDA_USER_NAME')};app_authorization={okta_token}"
    }

    logger.info("Generating pre-signed URL...")

    pre_signed_url = requests.post(
        url=f"{self.base_url}/presignedUrl",
        json={
            "fileName": file_name,
            "identifiers": identifiers
        },
        headers=headers,
        verify=False
    )

    if pre_signed_url.status_code != 200:
        raise Exception(f"Status Code: {pre_signed_url.status_code}; Response: {pre_signed_url.json()}")

    logger.info("Uploading file to S3...")

    response = requests.put(
        url=pre_signed_url.json()['url'],
        data=file,  # <-- this is the important part
        headers={"Content-Type": "application/octet-stream"},
        verify=False
    )

    if response.status_code != 200:
        raise Exception(f"Upload failed: {response.status_code}; {response.json()}")

    logger.info("File uploaded successfully!")