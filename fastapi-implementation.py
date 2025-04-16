import os
import json
import yaml
import csv
import pandas as pd
from typing import Dict, List, Any


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


class Document:
    def __init__(self, page_content=None, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}
    
    def __repr__(self):
        return f"Document(metadata={self.metadata}, page_content={self.page_content})"


class DataProcessor:
    def __init__(self):
        self.config = None
        self.table_meta = {}
        self.meta_values = []
        self.column_docs = []
        self.val_docs = []
        self.df = None
        
    def load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                self.config = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Config file {config_path} not found, creating default")
            # Create default config
            self.config = {
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
                yaml.dump(self.config, f)
        
        print("Configuration loaded successfully")
        return self.config
    
    def create_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.config['paths']['metadata'], exist_ok=True)
        os.makedirs(self.config['paths']['values'], exist_ok=True)
        os.makedirs(os.path.dirname(self.config['paths']['output']), exist_ok=True)
    
    def read_metadata(self):
        """Read metadata from JSON files"""
        meta_path = self.config['paths']['metadata']
        for filekey in os.listdir(meta_path):
            if not filekey.endswith('.json'):
                continue
            table_name = filekey.split('.')[0]
            with open(os.path.join(meta_path, filekey), 'r') as f:
                data = json.load(f)
                if 'name' not in data:
                    data['name'] = table_name
                self.table_meta[table_name] = TableInfo().from_dict(data)
                print(f"Loaded metadata for table: {table_name}")
        return self.table_meta
    
    def read_values(self):
        """Read values from JSON files"""
        values_path = self.config['paths']['values']
        for filekey in os.listdir(values_path):
            if not filekey.endswith('.json'):
                continue
            with open(os.path.join(values_path, filekey), 'r') as f:
                data = json.load(f)
                if 'table' in data and 'values' in data:
                    self.meta_values.append(data)
                    print(f"Loaded values for table: {data['table']}")
        return self.meta_values
    
    def column_to_document(self, column_info: ColumnInfo, table_info: TableInfo):
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
    
    def value_document(self, table_name, column_name, value):
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
    
    def process_column_metadata(self):
        """Process column metadata into documents"""
        self.column_docs = []
        for t in self.table_meta:
            for c in self.table_meta[t].columns:
                # Exclude meaningless columns unless they are key columns or metrics
                if c in ['obligor_id', 'oblgr_id', 'corp_oblgr_id', 'corp_clnt_org_id', 'id', 'case_id', 'rated_company_id']:
                    # Check if this column is a key column or metric
                    is_key = False
                    for key_col in self.table_meta[t].key_columns:
                        if key_col.name == c:
                            is_key = True
                            break
                    for key_metric in self.table_meta[t].key_metrics:
                        if key_metric.name == c:
                            is_key = True
                            break
                    if not is_key:
                        continue
                self.column_docs.append(self.column_to_document(self.table_meta[t].columns[c], self.table_meta[t]))
        return self.column_docs
    
    def process_values(self):
        """Process values into documents"""
        self.val_docs = []
        for vals in self.meta_values:
            for col in vals.get('values', {}):
                for v in vals['values'][col]:
                    self.val_docs.append(self.value_document(vals['table'], col, v))
        return self.val_docs
    
    def create_dataframe(self):
        """Create a pandas DataFrame from processed documents"""
        # Create lists for each column
        metadata_list = []
        content_list = []
        metadata_type_list = []
        
        # Add column metadata
        for doc in self.column_docs:
            metadata_list.append(str(doc.metadata))
            content_list.append(doc.page_content)
            metadata_type_list.append('table_meta')
        
        # Add values
        for doc in self.val_docs:
            metadata_list.append(str(doc.metadata))
            content_list.append(doc.page_content)
            metadata_type_list.append('table_values')
        
        # Create DataFrame
        self.df = pd.DataFrame({
            'metadata': metadata_list,
            'content': content_list,
            'metadata_type': metadata_type_list
        })
        
        print(f"Created DataFrame with {len(self.df)} rows")
        return self.df
    
    def to_csv(self):
        """Export DataFrame to CSV"""
        if self.df is None:
            print("DataFrame is not created yet. Call create_dataframe() first.")
            return False
            
        output_path = self.config['paths']['output']
        self.df.to_csv(output_path, index=False)
        print(f"Data exported successfully to {output_path}")
        return True
    
    def process_data(self):
        """Process all data and create DataFrame"""
        self.create_directories()
        self.read_metadata()
        self.read_values()
        self.process_column_metadata()
        self.process_values()
        return self.create_dataframe()
    
    def run(self, config_path: str = "configs/config.yml"):
        """Run the entire data processing pipeline"""
        self.load_config(config_path)
        self.process_data()
        self.to_csv()
        print("Pipeline execution completed successfully")
        return True


def main():
    processor = DataProcessor()
    return processor.run()


if __name__ == "__main__":
    main()