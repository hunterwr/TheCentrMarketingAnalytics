import streamlit as st
import pandas as pd
import plotnine
import pymongo

@st.cache
def get_data():
    return pd.read_csv("lead_logs.csv")
df = get_data()


# Show a table of the entire dataset.
st.write("## Our dataset:")
st.write(df)