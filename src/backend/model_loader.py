"""
Model loader module for handling pickle model loading
Implements singleton pattern for efficient memory usage
"""

import pickle
from pathlib import Path
from typing import Optional, Tuple, Any
import logging

import pandas as pd

from src.backend.config import PIPELINE_PATH, DATAFRAME_PATH

# Configure logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelLoader:
    """Singleton class for loading and caching ML models"""
    
    _instance: Optional['ModelLoader'] = None
    _pipeline: Optional[Any] = None
    _dataframe: Optional[pd.DataFrame] = None
    
    def __new__(cls):
        """Implement singleton pattern"""
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance
    
    def load_models(self) -> Tuple[Any, pd.DataFrame]:
        """
        Load pickle models with caching
        
        Returns:
            Tuple containing (pipeline, dataframe)
            
        Raises:
            FileNotFoundError: If model files are not found
            Exception: If pickle loading fails
        """
        if self._pipeline is None or self._dataframe is None:
            logger.info("Loading models from disk...")
            
            # Validate file existence
            if not PIPELINE_PATH.exists():
                raise FileNotFoundError(f"Pipeline model not found at {PIPELINE_PATH}")
            
            if not DATAFRAME_PATH.exists():
                raise FileNotFoundError(f"DataFrame not found at {DATAFRAME_PATH}")
            
            try:
                # Load pipeline
                with open(PIPELINE_PATH, 'rb') as f:
                    self._pipeline = pickle.load(f)
                logger.info(f"Pipeline loaded successfully from {PIPELINE_PATH}")
                
                # Load dataframe
                with open(DATAFRAME_PATH, 'rb') as f:
                    self._dataframe = pickle.load(f)
                logger.info(f"DataFrame loaded successfully from {DATAFRAME_PATH}")
                
            except Exception as e:
                logger.error(f"Error loading models: {str(e)}")
                raise Exception(f"Failed to load models: {str(e)}")
        
        return self._pipeline, self._dataframe
    
    def get_pipeline(self) -> Any:
        """Get the loaded pipeline model"""
        if self._pipeline is None:
            self.load_models()
        return self._pipeline
    
    def get_dataframe(self) -> pd.DataFrame:
        """Get the loaded dataframe"""
        if self._dataframe is None:
            self.load_models()
        return self._dataframe
    
    def reload_models(self) -> Tuple[Any, pd.DataFrame]:
        """
        Force reload models from disk
        
        Returns:
            Tuple containing (pipeline, dataframe)
        """
        logger.info("Forcing model reload...")
        self._pipeline = None
        self._dataframe = None
        return self.load_models()


# Global instance
model_loader = ModelLoader()