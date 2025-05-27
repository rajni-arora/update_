def move_objects_with_timestamp(self, source_folder, target_folder, filenames):
    try:
        logger.info(f"Moving specific objects from {source_folder} to {target_folder}...")
        from datetime import datetime

        for filename in filenames:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base, ext = os.path.splitext(filename)
            new_filename = f"{base}_{timestamp}{ext}"

            source_file_path = os.path.join(source_folder, filename)
            target_file_path = os.path.join(target_folder, new_filename)

            try:
                self.copy_object(source_file_path, target_file_path)
                logger.info(f"Copied: {source_file_path} to {target_file_path}")
                self.delete_object(source_file_path)
                logger.info(f"Deleted: {source_file_path}")
            except Exception as e:
                logger.error(f"Error moving file {filename}: {e}")
                raise

        logger.info("All specified objects moved successfully!")
    except Exception as e:
        logger.error(f"Error moving objects: {e}")
        raise HTTPException(status_code=500, detail=f"Error moving objects: {e}")