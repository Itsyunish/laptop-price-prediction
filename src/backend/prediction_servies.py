"""
Prediction service module containing business logic
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, Any

from src.backend.schema import LaptopSpecs
from src.backend.model_loader import model_loader

logger = logging.getLogger(__name__)


class PredictionService:
    def __init__(self):
        self.pipeline = model_loader.get_pipeline()

    @staticmethod
    def calculate_ppi(resolution: str, screen_size: float) -> float:
        x_res, y_res = map(int, resolution.split('x'))
        return ((x_res ** 2 + y_res ** 2) ** 0.5) / screen_size

    @staticmethod
    def preprocess_boolean(value: str) -> int:
        return 1 if value == "Yes" else 0

    def prepare_features(self, specs: LaptopSpecs) -> pd.DataFrame:
        """
        Prepare model-ready DataFrame (MATCHES TRAINING DATA)
        """
        X = pd.DataFrame([{
            "Company": specs.company,
            "TypeName": specs.type_name,
            "Ram": specs.ram,
            "Weight": specs.weight,
            "Touchscreen": self.preprocess_boolean(specs.touchscreen),
            "Ips": self.preprocess_boolean(specs.ips),
            "ppi": self.calculate_ppi(specs.resolution, specs.screen_size),
            "Cpu brand": specs.cpu,
            "HDD": specs.hdd,
            "SSD": specs.ssd,
            "Gpu brand": specs.gpu,
            "os": specs.os 
        }])

        return X

    def predict(self, specs: LaptopSpecs) -> float:
        try:
            X = self.prepare_features(specs)

            # Prediction (pipeline handles encoding)
            log_price = self.pipeline.predict(X)[0]

            predicted_price = np.exp(log_price)

            logger.info(f"Prediction successful: {predicted_price:.2f}")
            return float(predicted_price)

        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise Exception(f"Prediction failed: {str(e)}")

    def get_feature_options(self) -> Dict[str, Any]:
        df = model_loader.get_dataframe()
        return {
            "companies": sorted(df["Company"].unique().tolist()),
            "types": sorted(df["TypeName"].unique().tolist()),
            "cpu_brands": sorted(df["Cpu brand"].unique().tolist()),
            "gpu_brands": sorted(df["Gpu brand"].unique().tolist()),
            "operating_systems": sorted(df["os"].unique().tolist()),
        }


prediction_service = PredictionService() 
