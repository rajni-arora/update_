def to_csv(self):
    # Calling Indexing Pipeline
    indexing_payload = {
        "usecaseid": "1082",
        "usecasename": "gleam",
        "doc": {
            "metadata": {
                "origin": "doc uploaded from",
                "model_id": 111,
                "model_version": 1,
            }
        },
        "operation": {
            "embedding": "text-embedding-3-small",
            "chunking": {
                "type": None
            }
        },
        "metadata_cols": [
            "metadata_type",
            "table_name",
            "business_description",
            "usecase_id",
            "usecase_name",
            "dbname",
            "metadata_id",
            "meta_values",
            "start_index",
            "end_index",
            "doc_type",
            "input_type"
        ]
    }

    for file_path in [schema_output_path, knowledge_output_path, fewshot_output_path]:
        file_name = file_path.replace(output_path, "")

        if file_name.startswith("knowledge_"):
            indexing_payload["metadata_cols"] = [
                "metadata_type",
                "usecase_id",
                "usecase_name",
                "metadata_id",
                "meta_values",
                "start_index",
                "end_index",
                "doc_type",
                "input_type"
            ]

        elif file_name.startswith("fewshot_"):
            indexing_payload["metadata_cols"] = [
                "metadata_type",
                "usecase_id",
                "usecase_name",
                "metadata_id",
                "meta_values",
                "start_index",
                "end_index",
                "doc_type",
                "input_type"
            ]

        elif file_name.startswith("schema_"):
            # Keep default metadata_cols already set in initial payload
            pass

        else:
            logger.warning(f"Unknown file type for: {file_name}, skipping...")
            continue

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
                try:
                    os.remove(file_path)
                    logger.info(f"Deleted file after successful indexing: {file_path}")
                except Exception as e:
                    logger.error(f"Failed to delete file {file_path}: {e}")