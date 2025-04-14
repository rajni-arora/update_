import os
import json
import csv
import yaml

def load_config(config_path: str) -> dict:
    """Load YAML configuration from the specified path."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def read_json_files(directory_path: str) -> list:
    """Read all JSON files from a directory and return their contents."""
    results = []
    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return results
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, 'r') as f:
                    content = json.load(f)
                    results.append(content)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    return results

def process_and_write_csv(meta_dir: str, values_dir: str, output_csv: str) -> bool:
    """Process JSON files from meta and values directories and write to CSV."""
    # Read JSON files from meta directory
    meta_contents = read_json_files(meta_dir)
    
    # Read JSON files from values directory
    values_contents = read_json_files(values_dir)
    
    # Write to CSV
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            # Write header
            csv_writer.writerow(['content', 'datatype'])
            
            # Write meta data
            for content in meta_contents:
                csv_writer.writerow([json.dumps(content), 'meta'])
            
            # Write values data
            for content in values_contents:
                csv_writer.writerow([json.dumps(content), 'values'])
        
        print(f"CSV file created successfully: {output_csv}")
        return True
    except Exception as e:
        print(f"Error writing CSV file: {e}")
        return False

def main():
    # Load Configuration
    config_path = "config.yml"  # Update this path if needed
    try:
        config = load_config(config_path)
        print("Configuration loaded successfully")
        
        # Extract paths from config
        assets_dir = config.get('assets_directory', '')
        output_csv = config.get('output_csv', 'output.csv')
        
        # Construct full paths for meta and values directories
        meta_dir = os.path.join(assets_dir, 'meta')
        values_dir = os.path.join(assets_dir, 'values')
        
        # Process data and create CSV
        result = process_and_write_csv(meta_dir, values_dir, output_csv)
        print("Pipeline execution completed successfully") if result else print("Pipeline execution failed")
        
        return result
    except Exception as e:
        print(f"Error in main function: {e}")
        return False

if __name__ == "__main__":
    main()