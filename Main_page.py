import streamlit as st
import pandas as pd
from plotnine import *
import pymongo
from pymongo import MongoClient

@st.cache
def get_data():
    return pd.read_csv("lead_logs.csv")
df = get_data()


# Show a table of the entire dataset.
st.write("## Our dataset:")
st.write(df)

def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

cluster = init_connection()

db = cluster['datalake']

collection = db['facebook-ad-datas']

results = collection.find({})

temp_df = pd.DataFrame()

for result in results:
    ad_data = result    #['data'] #['data'] #['data']
    df = pd.json_normalize(ad_data)
    temp_df = pd.concat([temp_df, df], ignore_index=True)
temp_df.columns=temp_df.columns.str.replace('data.','')
temp_df['AmountSpent'] = pd.to_numeric(temp_df['Amount Spent'])

final_df = temp_df

gph = ggplot(data=final_df, mapping=aes(x='Day', y ='AmountSpent', fill='Ad Name') + geom_bar(stat='identity') + theme_classic() + theme(axis_text_x=element_text(rotation=90, hjust=1)))

st.pyplot(ggplot.draw(gph))