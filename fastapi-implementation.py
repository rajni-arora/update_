def to_csv(self):
    combined_output_path = f"{output_path}/preprocessed_{timestamp}.csv"

    # Combine all dataframes horizontally
    combined_df = pd.concat([
        self.df1, self.df2, self.df3, self.df4, self.df5
    ], axis=1)

    # Add static values
    combined_df['usecase_id'] = '1082'
    combined_df['usecase_name'] = 'gleam'
    combined_df['dbname'] = 'cstonedb3'
    combined_df['metadata_id'] = [str(uuid.uuid4()) for _ in range(len(combined_df))]

    # Rearrange columns so that df1 and df2 come after metadata_id
    df1_cols = self.df1.columns.tolist()
    df2_cols = self.df2.columns.tolist()

    cols = combined_df.columns.tolist()

    # Remove df1 and df2 cols from current position
    for col in df1_cols + df2_cols:
        if col in cols:
            cols.remove(col)

    # Find the index of metadata_id
    metadata_index = cols.index('metadata_id') + 1

    # Insert df1 and df2 cols (preserving order) after metadata_id
    cols = cols[:metadata_index] + df1_cols + df2_cols + cols[metadata_index:]

    # Reorder the DataFrame
    combined_df = combined_df[cols]

    # Save to CSV
    combined_df.to_csv(combined_output_path, index=False)