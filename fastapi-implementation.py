def index_exists(self, index_name):
    query = f"""
    SELECT index_name FROM system_schema.indexes 
    WHERE keyspace_name = '{self.keyspace}' 
      AND table_name = '{self.table}';
    """
    rows = self.session.execute(query)
    return any(row.index_name == index_name for row in rows)

def drop_index(self, index_name):
    try:
        drop_query = f"DROP INDEX IF EXISTS {self.keyspace}.{index_name};"
        self.session.execute(drop_query)
        print(f"Dropped existing index: {index_name}")
    except Exception as e:
        print(f"Error dropping index {index_name}: {e}")

def create_vector_index(self, vector_column):
    try:
        # Connect if session/cluster is down
        if self.cluster.is_shutdown:
            self.cluster = Cluster(
                self.clusternode,
                auth_provider=PlainTextAuthProvider(username=USER_NAME, password=PASSWORD)
            )
        if self.session.is_shutdown:
            self.session = self.cluster.connect()
            self.session.set_keyspace(self.keyspace)

        # Build index name
        index_name = f"ann_index_{vector_column}"

        # Drop index if exists
        if self.index_exists(index_name):
            self.drop_index(index_name)

        # Create index
        index_query = f"""
        CREATE CUSTOM INDEX {index_name}
        ON {self.table} ({vector_column})
        USING 'StorageAttachedIndex'
        WITH OPTIONS = {{ 'similarity_function': 'COSINE' }};
        """
        self.session.execute(index_query)
        print(f"Created new index: {index_name}")

    except Exception as e:
        print(f"Error creating index: {e}")