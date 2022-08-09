import streamlit as st
import pandas as pd
from plotnine import *


@st.cache
def get_data():
    return pd.read_csv("lead_logs.csv")
df = get_data()


st.write(df)