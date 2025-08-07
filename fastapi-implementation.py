index_queries = {
    f"{table_name}_entries_map_sai": f"""
        CREATE CUSTOM INDEX {table_name}_entries_map_sai
        ON {table_name} (ENTRIES(entries))
        USING 'StorageAttachedIndex';
    """,
    f"{table_name}_keys_map_sai": f"""
        CREATE CUSTOM INDEX {table_name}_keys_map_sai
        ON {table_name} (ENTRIES(keys))
        USING 'StorageAttachedIndex';
    """,
    f"{table_name}_values_map_sai": f"""
        CREATE CUSTOM INDEX {table_name}_values_map_sai
        ON {table_name} (ENTRIES(values))
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