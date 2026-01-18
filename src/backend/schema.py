"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class LaptopSpecs(BaseModel):
    """Schema for laptop specifications input"""
    
    company: str = Field(..., description="Laptop brand/manufacturer")
    type: str = Field(..., description="Type of laptop")
    ram: Literal[2, 4, 6, 8, 12, 16, 24, 32, 64] = Field(..., description="RAM in GB")
    weight: float = Field(..., gt=0, description="Weight of laptop in kg")
    touchscreen: Literal['No', 'Yes'] = Field(..., description="Touchscreen availability")
    ips: Literal['No', 'Yes'] = Field(..., description="IPS display")
    screen_size: float = Field(..., ge=10.0, le=18.0, description="Screen size in inches")
    resolution: str = Field(..., description="Screen resolution (e.g., 1920x1080)")
    cpu: str = Field(..., description="CPU brand")
    hdd: Literal[0, 128, 256, 512, 1024, 2048] = Field(..., description="HDD capacity in GB")
    ssd: Literal[0, 8, 128, 256, 512, 1024] = Field(..., description="SSD capacity in GB")
    gpu: str = Field(..., description="GPU brand")
    os: str = Field(..., description="Operating system")
    
    @validator('resolution')
    def validate_resolution(cls, v):
        """Validate resolution format"""
        try:
            parts = v.split('x')
            if len(parts) != 2:
                raise ValueError("Resolution must be in format 'WIDTHxHEIGHT'")
            int(parts[0])
            int(parts[1])
            return v
        except (ValueError, AttributeError):
            raise ValueError("Invalid resolution format")
    
    class Config:
        schema_extra = {
            "example": {
                "company": "Dell",
                "type": "Notebook",
                "ram": 8,
                "weight": 1.5,
                "touchscreen": "No",
                "ips": "Yes",
                "screen_size": 15.6,
                "resolution": "1920x1080",
                "cpu": "Intel Core i5",
                "hdd": 0,
                "ssd": 256,
                "gpu": "Intel",
                "os": "Windows"
            }
        }


class PredictionResponse(BaseModel):
    """Schema for prediction response"""
    
    predicted_price: float = Field(..., description="Predicted laptop price")
    currency: str = Field(default="USD", description="Currency of the price")
    specifications: LaptopSpecs = Field(..., description="Input specifications used for prediction")
    
    class Config:
        schema_extra = {
            "example": {
                "predicted_price": 45000.50,
                "currency": "USD",
                "specifications": {
                    "company": "Dell",
                    "type": "Notebook",
                    "ram": 8,
                    "weight": 1.5,
                    "touchscreen": "No",
                    "ips": "Yes",
                    "screen_size": 15.6,
                    "resolution": "1920x1080",
                    "cpu": "Intel Core i5",
                    "hdd": 0,
                    "ssd": 256,
                    "gpu": "Intel",
                    "os": "Windows"
                }
            }
        }


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    
    error: str = Field(..., description="Error message")
    detail: str = Field(None, description="Detailed error information")