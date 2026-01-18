"""
FastAPI application for Laptop Price Prediction
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from src.backend.schema import LaptopSpecs, PredictionResponse, ErrorResponse
from src.backend.prediction_servies import prediction_service
from config import API_TITLE, API_VERSION, API_DESCRIPTION

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Load models on startup"""
    logger.info("Starting up API server...")
    try:
        prediction_service.get_feature_options()
        logger.info("Models loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load models: {str(e)}")
        raise


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check"""
    return {
        "status": "healthy",
        "message": "Laptop Price Prediction API is running",
        "version": API_VERSION
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint"""
    try:
        # Verify models are loaded
        prediction_service.get_feature_options()
        return {
            "status": "healthy",
            "models_loaded": True,
            "version": API_VERSION
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "models_loaded": False,
                "error": str(e)
            }
        )


@app.get("/features", tags=["Features"])
async def get_features():
    """
    Get available feature options for prediction
    
    Returns available values for categorical features like brands, CPU, GPU, etc.
    """
    try:
        options = prediction_service.get_feature_options()
        return {
            "status": "success",
            "data": options
        }
    except Exception as e:
        logger.error(f"Error fetching features: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch feature options: {str(e)}"
        )


@app.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    tags=["Prediction"]
)
async def predict_price(specs: LaptopSpecs):
    """
    Predict laptop price based on specifications
    
    Args:
        specs: LaptopSpecs object containing all laptop specifications
        
    Returns:
        PredictionResponse with predicted price and input specifications
        
    Raises:
        HTTPException: If prediction fails
    """
    try:
        logger.info(f"Received prediction request for {specs.company} {specs.type}")
        
        # Make prediction
        predicted_price = prediction_service.predict(specs)
        
        # Create response
        response = PredictionResponse(
            predicted_price=round(predicted_price, 2),
            currency="USD",
            specifications=specs
        )
        
        logger.info(f"Prediction successful: ${predicted_price:.2f}")
        
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid input: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn
    from config import API_HOST, API_PORT
    
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
        log_level="info"
    )