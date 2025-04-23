import os
import json
import yaml
import csv
import pandas as pd
from typing import Dict, List, Any

# Import ViewShot utilities
try:
    from utils.few_shot import load_questions_excel_save_csv, load_examples_csv
except ImportError:
    print("Warning: ViewShot utilities not found. Functionality will be limited.")
    load_questions_excel_save_csv = None
    load_examples_csv = None


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
        self.knowledge_base_entries = []
        self.column_docs = []
        self.val_docs = []
        self.kb_docs = []
        self.viewshot_docs = []
        
        # Dataframes
        self.df = None       # Main dataframe
        self.df1 = None      # Content dataframe
        self.df2 = None      # Meta values dataframe
        self.df3 = None      # Metadata type dataframe
        self.df4 = None      # Table name dataframe
        self.df5 = None      # Business description dataframe
        
        # Raw table descriptions
        self.table_descriptions = {}
        
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
                    'output': 'output/',
                    'kb_directory': 'assets/knowledge_base_data/',
                    'viewshot_input': 'assets/viewshot_data/input.xlsx',
                    'viewshot_dataset_name': 'ViewShot_Dataset'
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
        os.makedirs(self.config['paths']['output'], exist_ok=True)
        os.makedirs(self.config['paths']['kb_directory'], exist_ok=True)
        
        # Create viewshot directory if needed
        viewshot_dir = os.path.dirname(self.config['paths'].get('viewshot_input', 'assets/viewshot_data/input.xlsx'))
        os.makedirs(viewshot_dir, exist_ok=True)
    
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
                # Save the description for later use in df5
                self.table_descriptions[table_name] = data.get('description', '')
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
    
    def read_knowledge_base(self):
        """Read knowledge base data from JSON files"""
        kb_path = self.config['paths'].get('kb_directory', 'assets/knowledge_base_data/')
        
        # Check if directory exists
        if not os.path.exists(kb_path):
            print(f"Knowledge base directory {kb_path} not found")
            return []
        
        # Read knowledge base files
        for filekey in os.listdir(kb_path):
            if not filekey.endswith('.json'):
                continue
                
            with open(os.path.join(kb_path, filekey), 'r') as f:
                try:
                    data = json.load(f)
                    # Process the knowledge base entries
                    for key, entry in data.items():
                        if isinstance(entry, dict) and 'description' in entry:
                            # Create a knowledge base entry
                            kb_entry = {
                                'title': key,
                                'description': entry.get('description', ''),
                                'example': entry.get('example', '')
                            }
                            self.knowledge_base_entries.append(kb_entry)
                    print(f"Loaded knowledge base data from: {filekey}")
                except json.JSONDecodeError:
                    print(f"Error parsing JSON in file: {filekey}")
        
        return self.knowledge_base_entries
    
    def process_viewshot_data(self):
        """Process ViewShot data from Excel file"""
        # Check if ViewShot utilities are available
        if load_questions_excel_save_csv is None or load_examples_csv is None:
            print("ViewShot utilities not available. Skipping ViewShot processing.")
            return []
        
        # Get ViewShot input path from config
        viewshot_path = self.config['paths'].get('viewshot_input', '')
        dataset_name = self.config['paths'].get('viewshot_dataset_name', 'ViewShot_Dataset')
        
        if not viewshot_path or not os.path.exists(viewshot_path):
            print(f"ViewShot input file not found: {viewshot_path}")
            return []
        
        try:
            # Process the Excel file through ViewShot utilities
            print(f"Processing ViewShot data from: {viewshot_path}")
            viewshot_df = load_questions_excel_save_csv(viewshot_path, dataset_name)
            viewshot_list = load_examples_csv(viewshot_df)
            
            # Convert ViewShot examples to documents
            self.viewshot_docs = []
            for item in viewshot_list:
                # Create document from ViewShot item
                doc = Document(
                    page_content=f"\"Page_content\": {{{item.page_content}}}",
                    metadata=item.metadata
                )
                self.viewshot_docs.append(doc)
                
            print(f"Processed {len(self.viewshot_docs)} ViewShot examples")
            return self.viewshot_docs
            
        except Exception as e:
            print(f"Error processing ViewShot data: {str(e)}")
            return []
    
    def process_knowledge_base(self):
        """Process knowledge base entries into documents"""
        self.kb_docs = []
        
        for entry in self.knowledge_base_entries:
            title = entry.get('title', '')
            description = entry.get('description', '')
            
            # Create content with "Page_content" and values in curly braces
            content = f"\"Page_content\": {{**{title}**\n{description}}}"
            
            # Create document
            doc = Document(
                page_content=content,
                metadata={
                    'title': title,
                    'type': 'knowledge'
                }
            )
            
            self.kb_docs.append(doc)
            
        print(f"Processed {len(self.kb_docs)} knowledge base entries into documents")
        return self.kb_docs
    
    def column_to_document(self, column_info: ColumnInfo, table_info: TableInfo):
        """Convert column metadata to document format"""
        page_content_dict = {
            'description': column_info.description,
            'column_name': column_info.name,
            'table': table_info.name
        }
        
        doc = Document(
            page_content=f"\"Page_content\": {{{json.dumps(page_content_dict)}}}",
            metadata={
                'table': column_info.table,
                'dataset': column_info.dataset,
                'column': column_info.name
            }
        )
        return doc
    
    def value_document(self, table_name, column_name, value, dataset=None):
        """Convert value to document format"""
        # Convert value to string if necessary
        if not isinstance(value, str):
            value_str = str(value)
        else:
            value_str = value
        
        metadata = {
            'table': table_name,
            'column': column_name
        }
        
        # Add dataset if provided
        if dataset:
            metadata['dataset'] = dataset
            
        doc = Document(
            page_content=f"\"Page_content\": {{{value_str}}}",
            metadata=metadata
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
            table_name = vals.get('table', '')
            dataset_name = vals.get('dataset', '')
            for col in vals.get('values', {}):
                for v in vals['values'][col]:
                    self.val_docs.append(self.value_document(table_name, col, v, dataset_name))
        return self.val_docs
    
    def create_dataframes(self):
        """Create all required dataframes"""
        # Create lists for each column in main dataframe
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
            
        # Add knowledge base entries
        for doc in self.kb_docs:
            metadata_list.append(str(doc.metadata))
            content_list.append(doc.page_content)
            metadata_type_list.append('knowledge')
            
        # Add ViewShot entries
        for doc in self.viewshot_docs:
            metadata_list.append(str(doc.metadata))
            content_list.append(doc.page_content)
            metadata_type_list.append('viewshot')
        
        # Create main DataFrame (df)
        self.df = pd.DataFrame({
            'metadata': metadata_list,
            'content': content_list,
            'metadata_type': metadata_type_list
        })
        
        # Create df1 (Content dataframe)
        self.df1 = pd.DataFrame({'content': content_list})
        
        # Create df2 (Meta values dataframe)
        self.df2 = pd.DataFrame({'meta_values': metadata_list})
        
        # Create df3 (Metadata type dataframe)
        self.df3 = pd.DataFrame({'metadata_type': metadata_type_list})
        
        # Create df4 (Table name dataframe)
        # Extract table names from metadata strings using string parsing
        table_names = []
        for meta_str in metadata_list:
            # Find the table value in the metadata string
            if "'table':" in meta_str or "'table'" in meta_str:
                # Simple string parsing to extract table name
                parts = meta_str.split("'table':")
                if len(parts) > 1:
                    table_part = parts[1].split(",")[0].strip()
                    table_name = table_part.replace("'", "").replace('"', '').strip()
                else:
                    parts = meta_str.split("'table'")
                    if len(parts) > 1:
                        if ":" in parts[1]:
                            table_part = parts[1].split(":")[1].split(",")[0].strip()
                            table_name = table_part.replace("'", "").replace('"', '').strip()
                        else:
                            table_name = ""
                    else:
                        table_name = ""
            elif "'title':" in meta_str:
                # For knowledge base entries
                parts = meta_str.split("'title':")
                if len(parts) > 1:
                    title_part = parts[1].split(",")[0].strip()
                    table_name = title_part.replace("'", "").replace('"', '').strip()
                else:
                    table_name = ""
            else:
                table_name = ""
            
            table_names.append(table_name)
        
        self.df4 = pd.DataFrame({'table_name': table_names})
        
        # Create df5 (Business description dataframe)
        business_descriptions = []
        
        for i, meta_type in enumerate(metadata_type_list):
            if meta_type == 'table_meta':
                # Extract table name from metadata
                meta_str = metadata_list[i]
                table_name = table_names[i]  # Use the table name we already extracted above
                
                # Get the description
                description = self.table_descriptions.get(table_name, '')
                business_descriptions.append(description)
            elif meta_type == 'knowledge' or meta_type == 'viewshot':
                # For knowledge base entries and ViewShot, leave business description empty
                business_descriptions.append('')
            else:
                # For values, use empty string
                business_descriptions.append('')
        
        self.df5 = pd.DataFrame({'business_description': business_descriptions})
        
        print(f"Created all dataframes. Main DataFrame has {len(self.df)} rows")
        return self.df, self.df1, self.df2, self.df3, self.df4, self.df5
    
    def to_csv(self):
        """Export only the combined DataFrame to CSV"""
        if self.df is None:
            print("DataFrames are not created yet. Call create_dataframes() first.")
            return False
        
        # Skip exporting main dataframe (data.csv)
        
        # Export combined dataframe
        output_path = self.config['paths'].get('output', 'output/')
        
        # Ensure path ends with '/'
        if not output_path.endswith('/'):
            output_path += '/'
            
        combined_output_path = f"{output_path}combined_data.csv"
        
        # Combine all dataframes horizontally
        combined_df = pd.concat([
            self.df1, self.df2, self.df3, self.df4, self.df5
        ], axis=1)
        
        combined_df.to_csv(combined_output_path, index=False)
        print(f"Combined data exported to {combined_output_path}")
        
        return True
    
    def process_data(self):
        """Process all data and create dataframes"""
        self.create_directories()
        self.read_metadata()
        self.read_values()
        self.read_knowledge_base()
        self.process_viewshot_data()  # New method to process ViewShot data
        self.process_column_metadata()
        self.process_values()
        self.process_knowledge_base()
        return self.create_dataframes()
    
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