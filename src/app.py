import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load model and DataFrame
pipe = pickle.load(open('src/backend/pipe.pkl','rb'))
df = pickle.load(open('src/backend/df.pkl','rb'))

st.title("Laptop Price Predictor")

# Streamlit inputs
company = st.selectbox('Brand', df['Company'].unique())
type_name = st.selectbox('Type', df['TypeName'].unique())
ram = st.selectbox('RAM(in GB)', [2,4,6,8,12,16,24,32,64])
weight = st.number_input('Weight of the Laptop')
touchscreen = st.selectbox('Touchscreen',['No','Yes'])
ips = st.selectbox('IPS',['No','Yes'])
screen_size = st.slider('Screen Size in inches', 10.0, 18.0, 13.0)
resolution = st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])
cpu = st.selectbox('CPU', df['Cpu brand'].unique())
hdd = st.selectbox('HDD(in GB)', [0,128,256,512,1024,2048])
ssd = st.selectbox('SSD(in GB)', [0,8,128,256,512,1024])
gpu = st.selectbox('GPU', df['Gpu brand'].unique())
os = st.selectbox('OS', df['os'].unique())

if st.button('Predict Price'):
    # Convert Yes/No to numeric
    touchscreen_val = 1 if touchscreen == 'Yes' else 0
    ips_val = 1 if ips == 'Yes' else 0

    # Calculate PPI 
    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])
    ppi = ((X_res**2) + (Y_res**2))**0.5 / screen_size

    # Create DataFrame for prediction (match training df columns)
    query = pd.DataFrame([[company, type_name, ram, weight, touchscreen_val, ips_val, ppi, cpu, hdd, ssd, gpu, os]],
                         columns=['Company','TypeName','Ram','Weight','Touchscreen','Ips','ppi','Cpu brand','HDD','SSD','Gpu brand','os'])

    # Predict
    prediction = pipe.predict(query)[0]
    st.title(f"The predicted price of this configuration is ₹{int(np.exp(prediction))}")
