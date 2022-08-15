import streamlit as st
import pandas as pd
from plotnine import *
import pymongo
from pymongo import MongoClient
from datetime import datetime
from datetime import time

@st.cache
def get_data():
    return pd.read_csv("lead_logs.csv")
df = get_data()


# Show a table of the entire dataset.
#st.write("## Our dataset:")
#st.write(df)

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


#newdf = df[(df.origin >= "JFK") & (df.carrier == "B6")]

final_df = temp_df

gph = ggplot(data=final_df, mapping=aes(x='Day', y ='AmountSpent', fill='Ad Name')) + geom_bar(stat='identity') + theme_classic() + theme(axis_text_x=element_text(rotation=90, hjust=1))

st.markdown("## Ad Spend Summary")
temp_df['Datetime'] = pd.to_datetime(temp_df['Day'])
max_year = temp_df['Datetime'].max().year
max_month = temp_df['Datetime'].max().month
max_day = temp_df['Datetime'].max().day
min_year = temp_df['Datetime'].min().year
min_month = temp_df['Datetime'].min().month
min_day = temp_df['Datetime'].min().day

#values = st.slider("Select the date range", min_value=None, max_value=None, value=(min, max), step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False)

st.pyplot(ggplot.draw(gph))



start_time = st.slider(
     "When do you start?",
     value=datetime(2020, 1, 1, 9, 30),
     format="MM/DD/YY - hh:mm")
st.write("Start time:", start_time)





import streamlit as st
import datetime as dt
import pandas as pd



## Range selector
cols1,_ = st.beta_columns((1,2)) # To make it narrower
format = 'MMM DD, YYYY'  # format output
start_date = dt.date(year=2021,month=1,day=1)  #  I need some range in the past
end_date = dt.datetime.now().date()
max_days = end_date-start_date

slider = cols1.slider('Select date', min_value=start_date, value=end_date ,max_value=end_date, format=format)
## Sanity check
st.table(pd.DataFrame([[start_date, slider, end_date]],
                columns=['start',
                        'selected',
                        'end'],
                index=['date']))


st.write(min_year)
st.write(min_month)
st.write(min_day)