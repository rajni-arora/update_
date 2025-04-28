I'll edit the function to separate data into two CSV files based on the "metadata_type" column. Let me create a more focused update:

```python
def to_csv(self):
    """Export DataFrame to CSV"""
    if self.df is None:
        print("DataFrames are not created yet. Call create_dataframes() first.")
        return False
        
    # Export main dataframe
    output_path = self.config['paths'].get('output', 'output/')
    
    # Create paths for schema and knowledge files
    schema_output_path = f"{output_path}schema.csv"
    knowledge_output_path = f"{output_path}knowledge.csv"
    
    # Separate data based on metadata_type
    knowledge_df = combined_df[combined_df['metadata_type'] == 'knowledge']
    schema_df = combined_df[combined_df['metadata_type'].isin(['few_shot', 'meta', 'values'])]
    
    # Export schema dataframe
    schema_df.to_csv(schema_output_path, index=False, sep='|')
    print(f"Schema data exported to: {schema_output_path}")
    
    # Export knowledge dataframe
    knowledge_df.to_csv(knowledge_output_path, index=False, sep='|')
    print(f"Knowledge data exported to: {knowledge_output_path}")
    
    return True
```

Here are the specific changes needed:

Old lines:
```python
# Export combined dataframe
from datetime import import datetime
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#output_file = os.path.join(output_path, f"schema{timestamp}.csv")
combined_output_path = f"{output_path}preprocessed_{timestamp}.csv"

# ... reordering code ...

combined_df.to_csv(combined_output_path, index=False, sep='|')
print(f"Combined data exported to: {combined_output_path}")
```

New lines:
```python
# Create paths for schema and knowledge files
schema_output_path = f"{output_path}schema.csv"
knowledge_output_path = f"{output_path}knowledge.csv"

# Separate data based on metadata_type
knowledge_df = combined_df[combined_df['metadata_type'] == 'knowledge']
schema_df = combined_df[combined_df['metadata_type'].isin(['few_shot', 'meta', 'values'])]

# Export schema dataframe
schema_df.to_csv(schema_output_path, index=False, sep='|')
print(f"Schema data exported to: {schema_output_path}")

# Export knowledge dataframe
knowledge_df.to_csv(knowledge_output_path, index=False, sep='|')
print(f"Knowledge data exported to: {knowledge_output_path}")
```

This will:
1. Create two fixed filenames: "schema.csv" and "knowledge.csv" in the output directory
2. Filter the combined dataframe by "metadata_type" values
3. Save "knowledge" data to knowledge.csv
4. Save "few_shot", "meta", and "values" data to schema.csv
5. Use the '|' separator as in your original code​​​​​​​​​​​​​​​​