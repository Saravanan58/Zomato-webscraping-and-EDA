from pandas.core.arrays.integer import Int64Dtype
from pandas.io.formats.format import IntArrayFormatter
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px

df_prefinal = pd.read_csv("zomato_prefinal.csv")
df_final = pd.read_csv("zomato_final.csv")

st.write('''
# Zomato Webscraping and EDA of Coimbatore restaurants
### Sample Dataset obtained from webscraping the zomato site
 ''')

st.write('''
-------------------
##### Feature Description\n
 * rest_name: Restaurant name
 * rating: Restaurant rating
 * pro_offer: Offer for Zomato-Pro users
 * offer: Offer for all Zomato users
 * del_time: Approx. delivery time
 * category: Restaurant dish category
 * cost_for_one: Approx. Food cost for one person
 * recent_orders_count: Recent order stats displayed by Zomato
 * lat: GPS latitude coordinatess
 * long: GPS longitude coordinates
 \n----------------''')

st.dataframe(df_final)
df_final.rename(columns={"long":"lon"},inplace=True)
st.write("#### Restaurants density in Coimbatore")
st.map(df_final[["lat","lon"]].dropna())



fig = px.bar(data_frame = df_final[['rest_name','rating']].dropna().sort_values('rating', ascending =False)[:10],x = "rest_name", y="rating")
fig.write_html('first_figure.html')
st.plotly_chart(fig, use_container_width=True)