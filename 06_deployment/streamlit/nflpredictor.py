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
#st.balloons()
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

df_global = pd.read_csv('results_games_2022.csv')
df_global = df_global.loc[(df_global.week==global_weeks)]
df_global = df_global.replace("Commanders", "Washington")
df_global.reset_index()

col1 , col_away_team, col_home_team , col_winner , col5 = st.columns(5)

with st.container():
    with col1:
        st.write(' ')
    with col_away_team:
        st.caption("Away team")
    with col_home_team:
        st.caption("Home team")
    with col_winner:
        st.caption("Winner")
    with col5:
        st.write(' ')

for index,row in df_global.iterrows():
    with st.container():
        with col1:
            st.write(' ')
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
        with col_winner:
            if(row['winner']==1):
                image = Image.open('src/'+row['hometeam']+'.png')
                st.image(image,width=32)
                st.text(row['hometeam']) 
            else:
                image = Image.open('src/'+row['awayteam']+'.png')
                st.image(image,width=32)
                st.text(row['awayteam'])  
            #image = Image.open('06_deployment/src/'+row['hometeam']+'.png')
            #st.image(image)
        with col5:
            st.write(' ')

        #st.text(games)


#df_global_cleaned = df_global[['awayteam','hometeam','winner']]
#with st.container():
#        global_weeks = st.table(df_global_cleaned)

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
    st.markdown("<p style='text-align: center;'>"+stadium+"</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>"+location+"</p>", unsafe_allow_html=True)

#df_stats = pd.read_csv('espn_scores.json')
col_away_detail, col_home_detail = st.columns(2)

with st.container():  
    with col1:
        st.write(' ')  
    with col_away_detail:
        #st.markdown("<h1 style='text-align: center; color: red;'>Some title</h1>", unsafe_allow_html=True)
        image = Image.open('src/'+away_team+'.png')
        st.image(image)
        #st.text(away_team)
        st.markdown("<p style='text-align: center;'>"+away_team+"</p>", unsafe_allow_html=True)
        #st.markdown("<h1 style='text-align: center; color: red;'>"+away_team+"</h1>", unsafe_allow_html=True)
        #st.markdown('pouet1')
        #col1, col2= st.columns(2)
        #col1.metric("2021 Away victories", "70 °F", "1.2 °F")
        #col2.metric("2021 biggest win streak", "9 mph", "-8%")
    with col_home_detail:
        image = Image.open('src/'+home_team+'.png')
        st.image(image)
        #st.markdown("<p style='text-align: center;'>"+st.image(image)+"</p>", unsafe_allow_html=True)
        #st.text(home_team)
        st.markdown("<p style='text-align: center;'>"+home_team+"</p>", unsafe_allow_html=True)
        #st.markdown("<h1 style='text-align: center; color: red;'>"+home_team+"</h1>", unsafe_allow_html=True)
        #st.markdown('pouet2')mù
        #col1, col2 = st.columns(2)
        #col1.metric("2021 Home victories", "70 °F", "1.2 °F")
        #col2.metric("2021 biggest win streak", "9 mph", "-8%")
    with col5:
        st.write(' ')
   