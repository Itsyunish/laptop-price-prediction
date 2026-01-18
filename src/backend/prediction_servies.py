"""
Prediction service module containing business logic
"""

import numpy as np
import logging
from typing import Dict, Any

from src.backend.schema import LaptopSpecs
from src.backend.model_loader import model_loader

logger = logging.getLogger(__name__) 


class PredictionService:
    """Service class for laptop price predictions"""
    
    def __init__(self):
        """Initialize the prediction service"""
        self.pipeline = model_loader.get_pipeline()
    
    @staticmethod
    def calculate_ppi(resolution: str, screen_size: float) -> float:
        """
        Calculate pixels per inch (PPI)
        
        Args:
            resolution: Screen resolution in format 'WIDTHxHEIGHT'
            screen_size: Screen size in inches
            
        Returns:
            Calculated PPI value
        """
        x_res, y_res = map(int, resolution.split('x'))
        ppi = ((x_res ** 2) + (y_res ** 2)) ** 0.5 / screen_size
        return ppi
    
    @staticmethod
    def preprocess_boolean(value: str) -> int:
        """
        Convert Yes/No to 1/0
        
        Args:
            value: 'Yes' or 'No' string
            
        Returns:
            1 for 'Yes', 0 for 'No'
        """
        return 1 if value == 'Yes' else 0
    
    def prepare_features(self, specs: LaptopSpecs) -> np.ndarray:
        """
        Prepare feature array for prediction
        
        Args:
            specs: LaptopSpecs object containing input specifications
            
        Returns:
            Numpy array of features ready for prediction 
        """
        # Convert boolean features
        touchscreen = self.preprocess_boolean(specs.touchscreen)
        ips = self.preprocess_boolean(specs.ips)
        
        # Calculate PPI
        ppi = self.calculate_ppi(specs.resolution, specs.screen_size)
        
        # Create feature array in correct order
        features = np.array([
            specs.company,
            specs.type,
            specs.ram,
            specs.weight,
            touchscreen,
            ips,
            ppi,
            specs.cpu,
            specs.hdd,
            specs.ssd,
            specs.gpu,
            specs.os
        ])
        
        # Reshape for prediction (1 sample, 12 features)
        features = features.reshape(1, 12)
        
        return features
    
    def predict(self, specs: LaptopSpecs) -> float:
        """
        Predict laptop price based on specifications
        
        Args:
            specs: LaptopSpecs object containing input specifications
            
        Returns:
            Predicted price
            
        Raises:
            Exception: If prediction fails
        """
        try:
            # Prepare features
            features = self.prepare_features(specs)
            
            # Make prediction
            log_price = self.pipeline.predict(features)[0]
            
            # Convert from log scale to actual price
            predicted_price = np.exp(log_price)
            
            logger.info(f"Prediction successful: {predicted_price:.2f}")
            
            return float(predicted_price)
            
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise Exception(f"Prediction failed: {str(e)}")
    
    def get_feature_options(self) -> Dict[str, Any]:
        """
        Get available options for categorical features
        
        Returns:
            Dictionary containing available options for each feature
        """
        df = model_loader.get_dataframe()
        
        return {
            'companies': sorted(df['Company'].unique().tolist()),
            'types': sorted(df['TypeName'].unique().tolist()),
            'cpu_brands': sorted(df['Cpu brand'].unique().tolist()),
            'gpu_brands': sorted(df['Gpu brand'].unique().tolist()),
            'operating_systems': sorted(df['os'].unique().tolist())
        }


# Global service instance
prediction_service = PredictionService()