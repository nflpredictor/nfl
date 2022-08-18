from optparse import Option
#from turtle import width
import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import datetime
import streamlit.components.v1 as components  # Import Streamlit
from PIL import Image



st.title('NFL Predictor 2022')

json_file = 'espn_2022calendar.json'

#file = open(json_file)
#data = json.load(file)

#print(os.listdir())

df = pd.read_json(json_file)
#print(df)

weeks = df['week'].unique()
weeks = np.sort(weeks)
weeks = pd.DataFrame(weeks)

#today = datetime.now()
#teams = df['awayteam'].unique()
#teams = np.sort(teams)
#teams = pd.DataFrame(teams)

with st.container():
        global_weeks = st.selectbox('Pick your week to show all the games',weeks)

games = df.loc[(df.week==global_weeks)]
games.reset_index()
#games = games.iloc[:,'away_team']
#week = df.loc[(df.week==global_weeks)]



col1 , col_away_team, col_home_team , col4= st.columns(4)
for index,row in games.iterrows():
    with st.container():
        #with col_away_logo:
            #image = Image.open('06_deployment/src/'+row['awayteam']+'.png')
            #st.image(image)
            #print(os.listdir())
        with col_away_team:
            #st.header("Away team")
            image = Image.open('src/'+row['awayteam']+'.png')
            st.image(image,width=32)
            st.text(row['awayteam'])
        with col_home_team:
            #st.header("Home team")
            image = Image.open('src/'+row['hometeam']+'.png')
            st.image(image,width=32)
            st.text(row['hometeam'])  
        #with col_home_logo:
            #image = Image.open('06_deployment/src/'+row['hometeam']+'.png')
            #st.image(image)

        #st.text(games)

col_left, col_right = st.columns(2)

with st.container():
    with col_left:
        week = st.selectbox('Pick your week',weeks)
    with col_right:
        teams = df.loc[(df.week==week)]
        awayteams = pd.DataFrame({'team':teams.awayteam.unique()})
        hometeams = pd.DataFrame({'team':teams.hometeam.unique()})
        teams_df = [awayteams, hometeams]
        teams = pd.concat(teams_df,ignore_index=True)
        teams = teams.sort_values(by=['team'])
        team = st.selectbox('Pick your team',teams)

game = df.loc[(df.week==week) & ((df.hometeam==team) | (df.awayteam==team))]

away_team = game.iloc[0]['awayteam']
home_team = game.iloc[0]['hometeam']
stadium = game.iloc[0]['stadium']
location = game.iloc[0]['location']

with st.container():
    st.markdown("<h1 style='text-align: center;'>"+stadium+"</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>"+location+"</h1>", unsafe_allow_html=True)

with st.container():    
    with col_left:
        #st.markdown("<h1 style='text-align: center; color: red;'>Some title</h1>", unsafe_allow_html=True)
        image = Image.open('src/'+row['awayteam']+'.png')
        st.image(image)
        st.text(row['awayteam'])
        #st.markdown("<h1 style='text-align: center; color: red;'>"+away_team+"</h1>", unsafe_allow_html=True)
        #st.markdown('pouet1')
    with col_right:
        image = Image.open('src/'+row['hometeam']+'.png')
        st.image(image)
        st.text(row['hometeam'])
        #st.markdown("<h1 style='text-align: center; color: red;'>"+home_team+"</h1>", unsafe_allow_html=True)
        #st.markdown('pouet2')