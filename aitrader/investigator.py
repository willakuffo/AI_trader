import streamlit as st
import pandas as pd
import pickle

st.title('Forex TimeSeries Model Maker')

uploaded_file = st.file_uploader('upload historical data',type = ['pickle','csv'],accept_multiple_files = False,
help = 'upload time series data')
print(uploaded_file)

if uploaded_file is not None:
    
    st.header('Data View')
    #st.write('interact with the data with your mouse')


    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file.name)
        st.write(data)

    elif uploaded_file.name.endswith('.pickle'):
        data = pickle.load(open(uploaded_file.name,'rb'))
        st.write(data)
    st.info('interact with the data with your mouse')

    st.header('Data Plot')
    #st.write('interact with the plot with your mouse')
    st.line_chart(data[['open','high','low','close']])
    st.info('interact with the plot with your mouse')
