# 1. First, update your config.yml file with the exact path:

paths:
  metadata: "assets/meta"
  values: "assets/values"
  output: "output/"
  kb_directory: "assets/knowledge_base_data/"
  viewshot_input: "C:/Users/sn1009/Downloads/gold_pairs_example.xlsx"  # Update with the exact path from your screenshot
  viewshot_dataset_name: "Gold_Dataset"  # Update with the dataset name shown in your screenshot

# 2. Modify the process_viewshot_data method to handle the path issue better:

def process_viewshot_data(self):
    """Process ViewShot data from Excel file"""
    # Check if ViewShot utilities are available
    if few_shot.load_questions_excel_save_csv is None or few_shot.load_examples_csv is None:
        print("ViewShot utilities not available. Skipping ViewShot processing.")
        return []
    
    # Get ViewShot input path from config
    viewshot_path = self.config['paths'].get('viewshot_input', '')
    dataset_name = self.config['paths'].get('viewshot_dataset_name', 'ViewShot_Dataset')
    
    print(f"Looking for ViewShot file at: {viewshot_path}")
    
    if not viewshot_path:
        print("ViewShot input path not specified in config")
        return []
        
    if not os.path.exists(viewshot_path):
        print(f"ViewShot input file not found at configured path: {viewshot_path}")
        # Try alternative path
        alt_path = "C:/Users/sn1009/Downloads/gold_pairs_example.xlsx"
        if os.path.exists(alt_path):
            print(f"Found file at alternative path: {alt_path}")
            viewshot_path = alt_path
        else:
            print(f"File not found at alternative path either: {alt_path}")
            # List files in downloads directory to help diagnose
            try:
                download_dir = "C:/Users/sn1009/Downloads/"
                if os.path.exists(download_dir):
                    print(f"Files in Downloads directory:")
                    for file in os.listdir(download_dir):
                        if file.endswith('.xlsx'):
                            print(f"  - {file}")
            except Exception as e:
                print(f"Error listing files: {str(e)}")
            return []
    
    try:
        # Process the Excel file through ViewShot utilities
        print(f"Processing ViewShot data from: {viewshot_path}")
        viewshot_df = few_shot.load_questions_excel_save_csv(viewshot_path, dataset_name)
        viewshot_list = few_shot.load_examples_csv(viewshot_df)
        
        # Convert ViewShot examples to documents
        self.viewshot_docs = []
        for item in viewshot_list:
            # Create document from ViewShot item
            doc = Document(
                page_content=f"\"page_content\": {{{item.page_content}}}",
                metadata=item.metadata
            )
            self.viewshot_docs.append(doc)
        
        print(f"Processed {len(self.viewshot_docs)} ViewShot examples")
        return self.viewshot_docs
        
    except Exception as e:
        print(f"Error processing ViewShot data: {str(e)}")
        return []