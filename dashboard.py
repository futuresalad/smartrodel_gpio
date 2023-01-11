import time  # to simulate a real time data, time loop
import pandas as pd  # read csv, df manipulation
import matplotlib.pyplot as plt
import streamlit as st  # 🎈 data web app development
import os

st.set_page_config(
    page_title="Smartrodel Dashboard",
    page_icon="✅",
    layout="wide",
)

csv_filenames = []
csv_columns = ['vl','vr','hl','hr']
selected_dataframe = pd.DataFrame()


st.title("Smartrodel Dashboard")

col1, col2 = st.columns([1,2])

with col1:
    
    for (dirpath, dirnames, filenames) in os.walk("./data_export", topdown=False):
        csv_filenames.extend(filenames)
       
    try:
        selected_csv = st.selectbox('Select file', csv_filenames, disabled=False)
        selected_dataframe = pd.read_csv(f'./data_export/{selected_csv}')
        
    except Exception as e: 
        print(e)

    with open(f'./data_export/{selected_csv}', "rb") as file:

        st.download_button(
            label="Download data as CSV",
            data=file,
            file_name=selected_csv,
            mime='text/csv',
        )

with col2:
    st.line_chart(selected_dataframe, y=csv_columns)