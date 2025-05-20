for file_path in [schema_output_path, knowledge_output_path, fewshot_output_path]:
    file_name = file_path.replace(output_path, "")

    # Choose embedding model based on filename prefix
    if file_name.startswith("knowledge_"):
        model = "text-embedding-ada-002"
    elif file_name.startswith("schema_"):
        model = "text-embedding-3-small"
    elif file_name.startswith("fewshot_"):
        model = "text-embedding"
    else:
        logger.warning(f"Unknown file type for: {file_name}, skipping...")
        continue

    # Build payload
    indexing_payload["operation"]["embedding"] = model

    if file_name.startswith("knowledge_"):
        indexing_payload["metadata_cols"] = [
            "metadata_type", "table_name", "business_description",
            "usecase_id", "usecase_name", "dbname", "metadata_id",
            "meta_values", "start_index", "end_index", "doc_type", "input_type"
        ]
    else:
        indexing_payload["metadata_cols"] = ["metadata_type"]

    with open(file_path, "rb") as f:
        files = {'file': (file_name, f, 'text/csv')}
        data = {
            "metadata": json.dumps(indexing_payload)
        }

        logger.info(f"Starting indexing file - Payload: {indexing_payload}")
        response_indexing = requests.post(
            f"{self.config['DEFAULT']['INDEXING_URL']}/csv",
            files=files,
            data=data,
            timeout=3600,
            verify=False
        )

    if response_indexing.status_code != 200:
        raise Exception(f"status_code={response_indexing.status_code}, detail={response_indexing.json()}")
    else:
        logger.info(f"Indexing successful. Response:\n{response_indexing.json()}")

    # Cleanup
    try:
        os.remove(file_path)
        logger.info(f"Deleted file after successful indexing: {file_path}")
    except Exception as e:
        logger.error(f"Error deleting file: {e}")