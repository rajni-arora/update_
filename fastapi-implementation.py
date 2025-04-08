from fastapi import FastAPI, HTTPException, Depends, Body, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
import pandas as pd
import json
import logging
import sys
import os
import glob
import datetime
import numpy as np
import yaml
import fastparquet
import pyarrow as pa
import pyarrow.parquet as pq
from redact.utils.processor import discover_unstructured

# Path setup (from your original code)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Data Processing API",
    description="API for data loading, schema management, and knowledge base operations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import your existing classes (assuming they're implemented elsewhere)
from preprocess import (
    DataLoader, 
    SchemaManager, 
    KnowledgeBaseIndexer,
    DataLoadingOrchestrator,
    SchemaOrchestractor,
    KnowledgeBaseOrchestrator,
    Router,
    load_config
)

# Pydantic models for request/response
class ConfigPath(BaseModel):
    config_path: str = Field(..., description="Path to configuration file")

class DataLoadRequest(BaseModel):
    source_path: str = Field(..., description="Path to source data")
    target_path: Optional[str] = Field(None, description="Path for processed output")
    config: Optional[Dict[str, Any]] = Field(None, description="Optional configuration overrides")

class SchemaRequest(BaseModel):
    data_path: str = Field(..., description="Path to data for schema inference")
    output_path: Optional[str] = Field(None, description="Path to save schema")
    schema_options: Optional[Dict[str, Any]] = Field(None, description="Schema generation options")

class IndexRequest(BaseModel):
    data_path: str = Field(..., description="Path to data for indexing")
    index_path: Optional[str] = Field(None, description="Path to save index")
    index_options: Optional[Dict[str, Any]] = Field(None, description="Indexing options")

class QueryRequest(BaseModel):
    query: str = Field(..., description="Query string")
    index_path: str = Field(..., description="Path to knowledge base index")
    options: Optional[Dict[str, Any]] = Field(None, description="Query options")

# Dependencies
def get_config(config_path: str = Query(...)):
    try:
        return load_config(config_path)
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid configuration: {str(e)}")

def get_data_loader():
    return DataLoader()

def get_schema_manager():
    return SchemaManager()

def get_knowledge_indexer():
    return KnowledgeBaseIndexer()

# Routes

@app.get("/")
async def root():
    return {"message": "Data Processing API", "version": "1.0.0"}

@app.post("/config")
async def load_configuration(request: ConfigPath):
    """Load and validate a configuration file"""
    try:
        config = load_config(request.config_path)
        return {"status": "success", "config": config}
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/data/load")
async def load_data(
    request: DataLoadRequest,
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Load and preprocess data from a source location"""
    try:
        orchestrator = DataLoadingOrchestrator(data_loader)
        result = orchestrator.process(
            source_path=request.source_path,
            target_path=request.target_path,
            config=request.config
        )
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/schema/generate")
async def generate_schema(
    request: SchemaRequest,
    schema_manager: SchemaManager = Depends(get_schema_manager)
):
    """Generate schema from data"""
    try:
        orchestrator = SchemaOrchestractor(schema_manager)
        schema = orchestrator.generate_schema(
            data_path=request.data_path,
            options=request.schema_options
        )
        
        if request.output_path:
            orchestrator.save_schema(schema, request.output_path)
            
        return {"status": "success", "schema": schema}
    except Exception as e:
        logger.error(f"Error generating schema: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/knowledge/index")
async def create_index(
    request: IndexRequest,
    indexer: KnowledgeBaseIndexer = Depends(get_knowledge_indexer)
):
    """Create knowledge base index from data"""
    try:
        orchestrator = KnowledgeBaseOrchestrator(indexer)
        index_path = orchestrator.create_index(
            data_path=request.data_path,
            index_path=request.index_path,
            options=request.index_options
        )
        return {"status": "success", "index_path": index_path}
    except Exception as e:
        logger.error(f"Error creating index: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/knowledge/query")
async def query_knowledge_base(request: QueryRequest):
    """Query the knowledge base"""
    try:
        router = Router()
        results = router.query(
            query=request.query,
            index_path=request.index_path,
            options=request.options
        )
        return {"status": "success", "results": results}
    except Exception as e:
        logger.error(f"Error querying knowledge base: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/discover")
async def discover_data(path: str = Query(..., description="Path to discover data")):
    """Discover unstructured data in a directory"""
    try:
        results = discover_unstructured(path)
        return {"status": "success", "discovered": results}
    except Exception as e:
        logger.error(f"Error discovering data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
