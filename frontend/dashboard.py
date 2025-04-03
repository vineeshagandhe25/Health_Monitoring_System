import streamlit as st
import pandas as pd

st.title("Health Monitoring Dashboard")
data = pd.read_csv("health_data.csv")
st.line_chart(data[['heart_rate', 'steps']])