"""
Streamlit application for Laptop Price Prediction
"""

import streamlit as st
import logging
import requests
from typing import Optional 

from src.backend.schema import LaptopSpecs
from src.backend.prediction_servies import prediction_service
from src.backend.config import (
    RAM_OPTIONS,
    HDD_OPTIONS,
    SSD_OPTIONS,
    RESOLUTION_OPTIONS, 
    BOOLEAN_OPTIONS,
    SCREEN_SIZE_MIN,
    SCREEN_SIZE_MAX,
    SCREEN_SIZE_DEFAULT
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Laptop Price Predictor",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_session_state():
    """Initialize session state variables"""
    if 'prediction_made' not in st.session_state:
        st.session_state.prediction_made = False
    if 'predicted_price' not in st.session_state:
        st.session_state.predicted_price = None
    if 'last_specs' not in st.session_state:
        st.session_state.last_specs = None


def load_feature_options():
    """Load available options for categorical features"""
    try:
        return prediction_service.get_feature_options()
    except Exception as e:
        st.error(f"Error loading feature options: {str(e)}")
        logger.error(f"Failed to load features: {str(e)}")
        st.stop() 


def create_input_form(options):
    """
    Create the input form for laptop specifications
    
    Args:
        options: Dictionary containing available options for categorical features
        
    Returns:
        LaptopSpecs object if form is submitted, None otherwise
    """
    with st.form("laptop_specs_form"):
        st.subheader("Enter Laptop Specifications")
        
        # Create two columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            company = st.selectbox(
                'Brand',
                options=options['companies'],
                help="Select the laptop manufacturer"
            )
            
            laptop_type = st.selectbox(
                'Type',
                options=options['types'],
                help="Select the type of laptop"
            )
            
            ram = st.selectbox(
                'RAM (GB)',
                options=RAM_OPTIONS,
                index=RAM_OPTIONS.index(8),
                help="Select RAM capacity"
            )
            
            weight = st.number_input(
                'Weight (kg)',
                min_value=0.5,
                max_value=5.0,
                value=2.0,
                step=0.1,
                help="Enter the weight of the laptop"
            )
            
            touchscreen = st.selectbox(
                'Touchscreen',
                options=BOOLEAN_OPTIONS,
                help="Does the laptop have a touchscreen?"
            )
            
            ips = st.selectbox(
                'IPS Display',
                options=BOOLEAN_OPTIONS,
                help="Does the laptop have an IPS display?"
            )
        
        with col2:
            screen_size = st.slider(
                'Screen Size (inches)',
                min_value=SCREEN_SIZE_MIN,
                max_value=SCREEN_SIZE_MAX,
                value=SCREEN_SIZE_DEFAULT,
                step=0.1,
                help="Select the screen size"
            )
            
            resolution = st.selectbox(
                'Screen Resolution',
                options=RESOLUTION_OPTIONS,
                index=RESOLUTION_OPTIONS.index('1920x1080'),
                help="Select the screen resolution"
            )
            
            cpu = st.selectbox(
                'CPU',
                options=options['cpu_brands'],
                help="Select the CPU brand"
            )
            
            hdd = st.selectbox(
                'HDD (GB)',
                options=HDD_OPTIONS,
                index=HDD_OPTIONS.index(0),
                help="Select HDD capacity"
            )
            
            ssd = st.selectbox(
                'SSD (GB)',
                options=SSD_OPTIONS,
                index=SSD_OPTIONS.index(256),
                help="Select SSD capacity"
            )
            
            gpu = st.selectbox(
                'GPU',
                options=options['gpu_brands'],
                help="Select the GPU brand"
            )
            
            os = st.selectbox(
                'Operating System',
                options=options['operating_systems'],
                help="Select the operating system"
            )
        
        # Submit button
        submitted = st.form_submit_button(
            "🔮 Predict Price",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            try:
                specs = LaptopSpecs(
                    company=company,
                    type_name=laptop_type,
                    ram=ram,
                    weight=weight, 
                    touchscreen=touchscreen,
                    ips=ips,
                    screen_size=screen_size,
                    resolution=resolution,
                    cpu=cpu,
                    hdd=hdd,
                    ssd=ssd,
                    gpu=gpu,
                    os=os  
                )
                return specs
            except Exception as e:
                st.error(f"Invalid input: {str(e)}")
                logger.error(f"Validation error: {str(e)}")
                return None
        
        return None 


def display_prediction(price: float, specs: LaptopSpecs):
    """
    Display the prediction results
    
    Args:
        price: Predicted price
        specs: Input specifications
    """
    st.success("✅ Prediction Complete!")
    
    # Display predicted price prominently
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            f"<h1 style='text-align: center; color: #4CAF50;'>{price:,.2f}</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center; font-size: 18px;'>Predicted Laptop Price</p>",
            unsafe_allow_html=True
        )
    st.markdown("---")
    
    # Display specifications summary
    with st.expander("📋 Specification Summary", expanded=True):
        spec_col1, spec_col2 = st.columns(2)
        
        with spec_col1:
            st.write(f"**Brand:** {specs.company}")
            st.write(f"**Type:** {specs.type_name}")
            st.write(f"**CPU:** {specs.cpu}")
            st.write(f"**GPU:** {specs.gpu}") 
            st.write(f"**RAM:** {specs.ram} GB")
            storage_info = f"**Storage:** {specs.hdd} GB HDD + {specs.ssd} GB SSD"
            st.write(storage_info)
        
        with spec_col2:
            screen_info = f"**Screen:** {specs.screen_size}\" {specs.resolution}"
            st.write(screen_info)
            st.write(f"**Touchscreen:** {specs.touchscreen}")
            st.write(f"**IPS:** {specs.ips}")
            st.write(f"**Weight:** {specs.weight} kg")
            st.write(f"**OS:** {specs.os}")


def main():
    """Main application logic"""
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("💻 Laptop Price Predictor")
    st.markdown(
        "Enter your desired laptop specifications below to get an estimated price prediction."
    )
    
    # Load feature options
    with st.spinner("Loading models..."):
        options = load_feature_options()
    
    # Sidebar information 
    with st.sidebar:
        st.header("ℹ️ About")
        st.info(
            "This application uses machine learning to predict laptop prices "
            "based on various specifications. Simply fill in the form and click "
            "'Predict Price' to get an estimate."
        )
        
        st.header("📊 Model Info")
        st.write("- **Model Type:** Regression")
        st.write("- **Features:** 12 specifications")
        st.write("- **Target:** Price")
    
    # Create input form and get specifications
    specs = create_input_form(options)
    
    # Make prediction if form was submitted
    if specs is not None:
        with st.spinner("Making prediction..."):
            try:
                # Prepare payload
                payload = specs.model_dump(by_alias=True)
                logger.info(f"Sending payload: {payload}")
                
                # Make API request
                response = requests.post(
                    "http://localhost:8000/predict",
                    json=payload,
                    timeout=10
                )
                response.raise_for_status()
                
                # Extract prediction
                result = response.json()
                predicted_price = result["predicted_price"]
                
                # Update session state
                st.session_state.predicted_price = predicted_price
                st.session_state.last_specs = specs
                st.session_state.prediction_made = True
                
                logger.info(f"Prediction successful: {predicted_price:.2f}")
                
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the API. Make sure FastAPI server is running on http://localhost:8000")
                logger.error("Connection error: API server not reachable")
                st.session_state.prediction_made = False
                
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. Please try again.")
                logger.error("Request timeout")
                st.session_state.prediction_made = False
                
            except requests.exceptions.HTTPError as e:
                st.error(f"❌ API Error: {e.response.status_code}")
                if hasattr(e, 'response') and e.response.text:
                    st.error(f"Details: {e.response.text}")
                logger.error(f"HTTP error: {str(e)}")
                st.session_state.prediction_made = False 
                
            except Exception as e:
                st.error(f"❌ Prediction failed: {str(e)}")
                logger.error(f"Prediction error: {str(e)}", exc_info=True)
                st.session_state.prediction_made = False
    
    # Display prediction results
    if st.session_state.prediction_made and st.session_state.last_specs is not None:
        display_prediction(st.session_state.predicted_price, st.session_state.last_specs)


if __name__ == "__main__":
    main()