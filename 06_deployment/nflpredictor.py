from optparse import Option
import streamlit as st
import pandas as pd
import numpy as np
import json
import os

st.title('NFL Predictor 2022')

json_file = '01_scraping/json/espn_2022calendar.json'

#file = open(json_file)
#data = json.load(file)

#print(os.listdir())

df = pd.read_json(json_file)
#print(df)

weeks = df['week'].unique()
weeks = np.sort(weeks)

teams = df['awayteam'].unique()
teams = np.sort(teams)

col_left, col_right = st.columns(2)

with st.container():
    with col_left:
        option = st.selectbox('Pick your week',weeks)
    with col_right:
        teams = st.selectbox('Pick your team',teams)

with st.container():
    with col_left:
        st.markdown('Away Team')
    with col_right:
        st.markdown('Home Team')