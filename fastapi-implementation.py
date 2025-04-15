import os
import json
import yaml
import csv
from typing import Dict, List, Any

# Import TableInfo from utils.schema
class TableInfo:
    def __init__(self) -> None:
        self.name = None
        self.dataset = None
        self.business_name = None
        self.description = None
        self.columns = {}
        self.column_order = []
        self.key_columns = []
        self.key_metrics = []
        self.mask = None
        
    def from_dict(self, table_dict):
        self.name = table_dict.get('name', None)
        self.dataset = table_dict.get('dataset', None)
        self.business_name = table_dict.get('business_name', self.name)
        self.description = table_dict.get('description', 'No description provided')
        
        # Process columns
        self.columns = {}
        if 'columns' in table_dict:
            for k, v in table_dict['columns'].items():
                # Create ColumnInfo object and store in columns dictionary
                self.columns[k] = ColumnInfo(
                    name=v.get('name', k),
                    data_type=v.get('data_type', 'string'),
                    table=self.name,
                    dataset=self.dataset,
                    description=v.get('description', f'Column {k}'),
                    sample_values=v.get('sample_values', [])
                )
        
        self.column_order = list(self.columns.keys())
        
        # Process key_columns
        self.key_columns = []
        for k in table_dict.get('key_columns', []):
            if k in self.columns:
                self.key_columns.append(self.columns[k])
        
        # Process key_metrics
        self.key_metrics = []
        for k in table_dict.get('key_metrics', []):
            if k in self.columns:
                self.key_metrics.append(self.columns[k])
                
        return self
        
    def get_columns_as_dict(self):
        return {k: self.columns[k].description for k in self.column_order}
        
    def __str__(self) -> str:
        return f'Table(name={self.name}, dataset={self.dataset})'

# Import ColumnInfo from utils.schema
class ColumnInfo:
    def __init__(self, name, data_type, table, dataset, description, sample_values) -> None:
        self.name = name
        self.data_type = data_type.upper() if data_type else "STRING"
        self.table = table
        self.dataset = dataset
        self.description = description
        self.sample_values = sample_values
        
    def __str__(self) -> str:
        return f'Column(table={self.table}, name={self.name})'

# Import Document from langchain_core.documents
class Document:
    def __init__(self, page_content=None, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}
    
    def __repr__(self):
        return f"Document(metadata={self.metadata}, page_content={self.page_content})"

def load_config(config_path: str) -> dict:
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Config file {config_path} not found, creating default")
        # Create default config
        default_config = {
            'paths': {
                'metadata': 'assets/meta',
                'values': 'assets/values',
                'output': 'output/data.csv'
            }
        }
        # Ensure directory exists
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        # Write default config
        with open(config_path, 'w') as f:
            yaml.dump(default_config, f)
        return default_config

def column_to_document(column_info: ColumnInfo, table_info: TableInfo):
    """Convert column metadata to document format"""
    page_content_dict = {
        'description': column_info.description,
        'column_name': column_info.name,
        'table': table_info.name
    }
    
    doc = Document(
        page_content=json.dumps(page_content_dict),
        metadata={
            'table': column_info.table,
            'dataset': column_info.dataset,
            'column': column_info.name
        }
    )
    return doc

def value_document(table_name, column_name, value):
    """Convert value to document format"""
    # Convert value to string if necessary
    if not isinstance(value, str):
        value_str = str(value)
    else:
        value_str = value
        
    doc = Document(
        page_content=value_str,
        metadata={
            'table': table_name,
            'column': column_name
        }
    )
    return doc

def main():
    # Load configuration
    config_path = "configs/config.yml"
    config = load_config(config_path)
    print("Configuration loaded successfully")
    
    # Get paths from config
    meta_path = config['paths']['metadata']
    values_path = config['paths']['values']
    output_path = config['paths']['output']
    
    # Ensure directories exist
    os.makedirs(meta_path, exist_ok=True)
    os.makedirs(values_path, exist_ok=True)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Read metadata
    table_meta = {}
    for filekey in os.listdir(meta_path):
        if not filekey.endswith('.json'):
            continue
        table_name = filekey.split('.')[0]
        with open(os.path.join(meta_path, filekey), 'r') as f:
            data = json.load(f)
            if 'name' not in data:
                data['name'] = table_name
            table_meta[table_name] = TableInfo().from_dict(data)
            print(f"Loaded metadata for table: {table_name}")
    
    # Process column metadata into documents
    column_docs = []
    for t in table_meta:
        for c in table_meta[t].columns:
            # Exclude meaningless columns unless they are key columns or metrics
            if c in ['obligor_id', 'oblgr_id', 'corp_oblgr_id', 'corp_clnt_org_id', 'id', 'case_id', 'rated_company_id']:
                # Check if this column is a key column or metric
                is_key = False
                for key_col in table_meta[t].key_columns:
                    if key_col.name == c:
                        is_key = True
                        break
                for key_metric in table_meta[t].key_metrics:
                    if key_metric.name == c:
                        is_key = True
                        break
                if not is_key:
                    continue
            column_docs.append(column_to_document(table_meta[t].columns[c], table_meta[t]))
    
    # Read values
    meta_values = []
    for filekey in os.listdir(values_path):
        if not filekey.endswith('.json'):
            continue
        with open(os.path.join(values_path, filekey), 'r') as f:
            data = json.load(f)
            if 'table' in data and 'values' in data:
                meta_values.append(data)
                print(f"Loaded values for table: {data['table']}")
    
    # Process values into documents
    val_docs = []
    value_dicts = meta_values
    for vals in value_dicts:
        for col in vals.get('values', {}):
            for v in vals['values'][col]:
                val_docs.append(value_document(vals['table'], col, v))
    
    # Write to CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['metadata', 'content', 'metadata_type'])
        
        # Write column metadata
        for doc in column_docs:
            writer.writerow([
                str(doc.metadata),
                doc.page_content,
                'table_meta'
            ])
        
        # Write values
        for doc in val_docs:
            writer.writerow([
                str(doc.metadata),
                doc.page_content,
                'table_values'
            ])
    
    print(f"Data exported successfully to {output_path}")
    print("Pipeline execution completed successfully")
    return True

if __name__ == "__main__":
    main()