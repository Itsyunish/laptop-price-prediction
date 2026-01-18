"""
Configuration module for Laptop Price Predictor
Contains all configuration constants and paths
"""

from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR
DATA_DIR = BASE_DIR

# Model paths 
PIPELINE_PATH = MODEL_DIR / "pipe.pkl"
DATAFRAME_PATH = DATA_DIR / "df.pkl"
# Feature configurations
RAM_OPTIONS = [2, 4, 6, 8, 12, 16, 24, 32, 64]
HDD_OPTIONS = [0, 128, 256, 512, 1024, 2048]
SSD_OPTIONS = [0, 8, 128, 256, 512, 1024]

RESOLUTION_OPTIONS = [
    '1920x1080',
    '1366x768',
    '1600x900',
    '3840x2160',
    '3200x1800',
    '2880x1800',
    '2560x1600',
    '2560x1440',
    '2304x1440'
]

BOOLEAN_OPTIONS = ['No', 'Yes']

# Screen size configuration
SCREEN_SIZE_MIN = 10.0
SCREEN_SIZE_MAX = 18.0
SCREEN_SIZE_DEFAULT = 13.0

# API configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
API_TITLE = "Laptop Price Prediction API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "API for predicting laptop prices based on specifications"