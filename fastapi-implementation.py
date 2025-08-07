from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Setup
cluster1_nodes = ['127.0.0.1']  # Replace with your actual nodes
USER_NAME = 'your_username'
PASSWORD = 'your_password'
keyspace = 'your_keyspace'
table_name = 'your_table'

# Connect
auth_provider = PlainTextAuthProvider(username=USER_NAME, password=PASSWORD)
cluster = Cluster(cluster1_nodes, auth_provider=auth_provider)
session = cluster.connect()
session.set_keyspace(keyspace)

# Drop table
session.execute(f"DROP TABLE IF EXISTS {keyspace}.{table_name};")
print(f"Table {keyspace}.{table_name} dropped successfully.")