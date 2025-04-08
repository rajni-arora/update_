from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from preprocess import main, load_config

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

        # Inject the config into the process (assuming your main() uses global config or reads this)
        # If your script isn't dynamic to config changes, refactor your `main()` accordingly.
        main()

        return {"status": "success", "message": "Data processing completed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))