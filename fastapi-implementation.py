from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uvicorn
from preprocess import main as preprocessing_main, load_config

app = FastAPI()

class InputPath(BaseModel):
    input_directory: str

@app.post("/process-data/")
def process_data(input_path: InputPath):
    try:
        # Load config
        config_path = os.path.join(os.path.dirname(__file__), "configs", "config.yml")
        config = load_config(config_path)

        # Override input directory from user input
        config["paths"]["data_directory"] = input_path.input_directory

        # Optionally: Write the modified config back or use it in preprocessing functions
        # If your preprocess.main() does not take config as input,
        # you may need to refactor it to do so for dynamic handling.

        preprocessing_main()  # Assuming it uses updated global config

        return {"status": "success", "message": "Data processing completed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def main():
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=True)

if __name__ == "__main__":
    main()