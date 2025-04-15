import os
import json
import yaml
import csv
from typing import Dict, List, Any

class ColumnInfo:
    def __init__(self, name, data_type, table, dataset, description, sample_values) -> None:
        self.name = name
        self.data_type = data_type.upper()
        self.table = table
        self.dataset = dataset
        self.description = description
        self.sample_values = sample_values
        self.mask = None
        
    def set_mask(self, table_mask, idx):
        self.mask = f'{table_mask}_col_{idx}'
        return
        
    def m_schema(self):
        if self.mask is None:
            raise ValueError(f'Mask not set for {self}')
        m_schema = [
            f'{{self.mask}}:{{self.data_type}}',
            f'{{self.description}}',
            f'Examples: {{self.sample_values}}'
        ]
        return ', '.join(m_schema)
        
    def __str__(self) -> str:
        return f'Column(table={{self.table}}, name={{self.name}}, mask={{self.mask}})'
        
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
        self.name = table_dict['name']
        self.dataset = table_dict['dataset']
        self.business_name = table_dict.get('business_name', self.name)  # Handle if business_name is missing
        self.description = table_dict.get('description', 'No description provided')  # Handle if description is missing
        
        # Process columns
        self.columns = {}
        for k, v in table_dict.get('columns', {}).items():
            # Ensure we have all required fields even if missing in the source
            column_data = {
                'name': v.get('name', k),
                'data_type': v.get('data_type', 'string'),
                'description': v.get('description', f'Column {k}'),
                'sample_values': v.get('sample_values', [])
            }
            self.columns[k] = ColumnInfo(
                table=self.name,
                dataset=self.dataset,
                **column_data
            )
        
        self.column_order = list(self.columns.keys())
        
        # Handle key_columns
        key_cols = table_dict.get('key_columns', [])
        self.key_columns = []
        for k in key_cols:
            if k in self.columns:
                self.key_columns.append(self.columns[k])
        
        # Handle key_metrics
        key_metrics = table_dict.get('key_metrics', [])
        self.key_metrics = []
        for k in key_metrics:
            if k in self.columns:
                self.key_metrics.append(self.columns[k])
                
        return self
        
    def get_columns_as_dict(self):
        return {k: self.columns[k].description for k in self.column_order}
        
    def set_mask(self, idx):
        self.mask = f'table_{idx}'
        for cidx, col in enumerate(self.column_order):
            self.columns[col].set_mask(self.mask, cidx+1)
        return
        
    def m_schema(self):
        if self.mask is None:
            raise ValueError(f'Mask not set for {self}')
        field_lines = []
        for col in self.column_order:
            field_lines.append(self.columns[col].m_schema())
        m_schema = [
            f'# Table: {self.mask}',
            f'# Business Name: {self.business_name}',
            f'# Description: {self.description}',
            '[',
            ',\n'.join(field_lines),
            ']'
        ]
        return '\n'.join(m_schema)
        
    def __str__(self) -> str:
        return f'Table(name={self.name}, dataset={self.dataset}), mask={self.mask})'

class test:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def read_local_metadata(self, location):
        table_meta = {}
        for filekey in os.listdir(location):
            if not filekey.endswith('.json'):
                continue
            table_name = filekey.split('.')[0]
            with open(os.path.join(location, filekey), 'r') as f:
                data = json.load(f)
                
                # Make sure the data has a name field
                if 'name' not in data:
                    data['name'] = table_name
                    
                table_meta[table_name] = TableInfo().from_dict(data)
                print(f"Loaded metadata for table: {table_name}")
                
        return table_meta
    
    def read_local_metavalue(self, location):
        value_meta = []
        for filekey in os.listdir(location):
            if not filekey.endswith('.json'):
                continue
            with open(os.path.join(location, filekey), 'r') as f:
                data = json.load(f)
                if 'table' in data and 'values' in data:
                    value_meta.append(data)
                    print(f"Loaded values for table: {data['table']}")
                else:
                    print(f"Warning: File {filekey} doesn't have expected 'table' and 'values' fields")
                
        return value_meta
        
    def column_to_document(self, column_info: ColumnInfo, table_info: TableInfo):
        page_content_dict = {
            'description': column_info.description,
            'column_name': column_info.name,
            'table': table_info.name,
            'data_type': column_info.data_type,
            'dataset': column_info.dataset
        }
        return page_content_dict
        
    def value_document(self, table_name, column_name, value):
        # Convert value to string to ensure it can be written to CSV
        if not isinstance(value, str):
            value_str = str(value)
        else:
            value_str = value
            
        return {
            'page_content': value_str,
            'metadata': {
                'table': table_name,
                'column': column_name
            }
        }
        
    def create_column_index(self, table_meta):
        column_docs = []
        for t in table_meta:
            for c in table_meta[t].columns:
                # Exclude meaningless columns only if not specifically needed
                if c in ['obligor_id', 'oblgr_id', 'corp_oblgr_id', 'corp_clnt_org_id', 'id', 'case_id'] and c not in table_meta[t].key_columns and c not in table_meta[t].key_metrics:
                    print(f"Excluding column {c} from table {t}")
                    continue
                column_docs.append(self.column_to_document(table_meta[t].columns[c], table_meta[t]))
                
        print(f"Created {len(column_docs)} column documents")
        return column_docs
        
    def create_value_index(self, value_dicts: List[Dict]):
        val_docs = []
        for vals in value_dicts:
            table_name = vals.get('table', '')
            dataset_name = vals.get('dataset', '')
            
            # Process each column in the values
            for col, values in vals.get('values', {}).items():
                # Process each value in the column
                for v in values:
                    val_docs.append(self.value_document(table_name, col, v))
                    
        print(f"Created {len(val_docs)} value documents")
        return val_docs
        
    def export_to_csv(self, column_docs, val_docs, output_path):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Define extended fieldnames to capture more metadata
        fieldnames = ['type', 'table', 'dataset', 'column_name', 'data_type', 'description', 'value']
        
        with open(output_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            # Write column metadata
            for doc in column_docs:
                writer.writerow({
                    'type': 'metadata',
                    'table': doc.get('table', ''),
                    'dataset': doc.get('dataset', ''),
                    'column_name': doc.get('column_name', ''),
                    'data_type': doc.get('data_type', ''),
                    'description': doc.get('description', ''),
                    'value': ''
                })
            
            # Write values
            for doc in val_docs:
                writer.writerow({
                    'type': 'value',
                    'table': doc['metadata'].get('table', ''),
                    'dataset': '',  # No dataset in value metadata
                    'column_name': doc['metadata'].get('column', ''),
                    'data_type': '',  # No data_type in value metadata
                    'description': '',
                    'value': doc.get('page_content', '')
                })
                
        print(f"CSV exported successfully to {output_path}")
        
def load_config(config_path: str) -> dict:
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    # Load Configuration
    config_path = "configs/config.yml"
    
    # Check if config file exists, if not create a default one
    if not os.path.exists(config_path):
        print(f"Config file {config_path} not found, creating default")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        default_config = {
            'paths': {
                'metadata': 'assets/meta',
                'values': 'assets/values',
                'output': 'output/data.csv'
            }
        }
        with open(config_path, 'w') as f:
            yaml.dump(default_config, f)
            
    config = load_config(config_path)
    print("Configuration loaded successfully")
    
    # Initialize test class
    test_obj = test(config)
    
    # Read metadata and values
    meta_path = config['paths']['metadata']
    values_path = config['paths']['values']
    output_path = config['paths']['output']
    
    # Ensure directories exist
    os.makedirs(meta_path, exist_ok=True)
    os.makedirs(values_path, exist_ok=True)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Reading metadata from {meta_path}")
    table_meta = test_obj.read_local_metadata(meta_path)
    
    print(f"Reading values from {values_path}")
    value_meta = test_obj.read_local_metavalue(values_path)
    
    # Process data
    print("Processing column metadata...")
    column_docs = test_obj.create_column_index(table_meta)
    
    print("Processing value data...")
    val_docs = test_obj.create_value_index(value_meta)
    
    # Export to CSV instead of creating FAISS index
    print(f"Exporting data to {output_path}")
    test_obj.export_to_csv(column_docs, val_docs, output_path)
    
    print("Pipeline execution completed successfully")
    return True

if __name__ == "__main__":
    main()