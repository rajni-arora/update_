for file_path in [schema_output_path, knowledge_output_path, fewshot_output_path]:
    file_name = file_path.replace(output_path, "")

    if file_name.startswith("knowledge_"):
        indexing_payload["metadata_cols"] = [
            "metadata_type", "usecase_id", "usecase_name", "metadata_id",
            "meta_values", "start_index", "end_index", "doc_type", "input_type"
        ]
        indexing_payload["operation"]["embedding"] = "text-embedding-ada-002"

    elif file_name.startswith("fewshot_"):
        indexing_payload["metadata_cols"] = [
            "metadata_type", "usecase_id", "usecase_name", "metadata_id",
            "meta_values", "start_index", "end_index", "doc_type", "input_type"
        ]
        indexing_payload["operation"]["embedding"] = "text-embedding"

    elif file_name.startswith("schema_"):
        indexing_payload["metadata_cols"] = ["metadata_type"]
        indexing_payload["operation"]["embedding"] = "text-embedding-3-small"

    else:
        logger.warning(f"Unknown file type for: {file_name}, skipping...")
        continue

    # Send request
    with open(file_path, "rb") as f:
        files = {'file': (file_name, f, 'text/csv')}
        data = {"metadata": json.dumps(indexing_payload)}

        logger.info(f"Starting indexing file - Payload: {indexing_payload}")
        response_indexing = requests.post(
            f"{self.config['DEFAULT']['INDEXING_URL']}/csv",
            files=files,
            data=data,
            timeout=3600,
            verify=False
        )

    # Response handling
    if response_indexing.status_code != 200:
        raise Exception(f"status_code={response_indexing.status_code}, detail={response_indexing.json()}")
    else:
        logger.info(f"Indexing successful. Response:\n{response_indexing.json()}")

    try:
        os.remove(file_path)
        logger.info(f"Deleted file after successful indexing: {file_path}")
    except Exception as e:
        logger.error(f"Error deleting file: {e}")