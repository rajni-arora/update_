def create_index(keyspace: str, table_name: str):
    # Connect
    cluster = Cluster(
        cluster1_nodes,
        auth_provider=PlainTextAuthProvider(username=USER_NAME, password=PASSWORD)
    )
    session = cluster.connect()
    session.set_keyspace(keyspace)

    # Helper function to drop index safely
    def drop_if_exists(index_name):
        check_query = f"""
        SELECT index_name FROM system_schema.indexes
        WHERE keyspace_name = '{keyspace}' AND table_name = '{table_name}';
        """
        rows = session.execute(check_query)
        if any(row.index_name == index_name for row in rows):
            session.execute(f"DROP INDEX IF EXISTS {keyspace}.{index_name};")
            print(f"Dropped existing index: {index_name}")

    # Index creation queries
    index_queries = {
        f"{table_name}_entry_sai": f"""
            CREATE CUSTOM INDEX {table_name}_entry_sai
            ON {table_name} (entries['mtd_vl_tx'])
            USING 'StorageAttachedIndex';
        """,
        f"{table_name}_key_sai": f"""
            CREATE CUSTOM INDEX {table_name}_key_sai
            ON {table_name} (keys['mtd_vl_tx'])
            USING 'StorageAttachedIndex';
        """,
        f"{table_name}_value_sai": f"""
            CREATE CUSTOM INDEX {table_name}_value_sai
            ON {table_name} (values['mtd_vl_tx'])
            USING 'StorageAttachedIndex';
        """,
        f"{table_name}_vector_sai": f"""
            CREATE CUSTOM INDEX {table_name}_vector_sai
            ON {table_name} (vctr_d)
            USING 'StorageAttachedIndex';
        """,
        f"{table_name}_usecase_id_sai": f"""
            CREATE CUSTOM INDEX {table_name}_usecase_id_sai
            ON {table_name} (us_cs_id)
            USING 'StorageAttachedIndex';
        """
    }

    # Drop if exists and then create
    for index_name, query in index_queries.items():
        drop_if_exists(index_name)
        session.execute(query)
        print(f"Created index: {index_name}")