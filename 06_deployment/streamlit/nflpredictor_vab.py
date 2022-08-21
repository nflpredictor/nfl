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

### DATA

#### Data calendar 

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

### TITLE AND TEXT

st.set_page_config(
    page_title="Game Predictor",
    page_icon="💸",
    layout="centered"
  )


st.title("NFL season 2022: which team will win the next game ? 🏈")

st.markdown("""
    Welcome to Game Predictor. Thanks to our awesome Machine Learning model we are going to help you 
    bet on the next NFL game. How ? Simple answer, choose the week, choose the game and enjoy the result!
    If you need an overview of the results per week, check our summary at the end of the page 👇
""")
st.text('')
st.text('')

### PREDICTION SECTION

df_global = pd.read_csv('results_games_2022_xgb.csv') # ATTENTION SI LE NOM DU FICHIER DE PREDICTION CHANGE, VENIR LE MODIFIER ICI
df_global['game'] = df_global[['hometeam', 'awayteam']].agg(' vs '.join, axis=1)

#full_dataset = pd.read_csv('../../04_datasets/nfl_dataset_vf.csv') #Update : Fichier csv passé dans le même dossier (Plus dans un dossier parent)
full_dataset = pd.read_csv('nfl_dataset_vf.csv')

global_weeks = df_global['week'].unique()
global_weeks = np.sort(global_weeks)
global_weeks = pd.DataFrame(global_weeks)

global_games = df_global['game'].unique()
global_games = np.sort(global_games)
global_games = pd.DataFrame(global_games)

col_left, col_right = st.columns(2)

with st.container():
    with col_left:
        week = st.selectbox('On which week do you want to place a bet?',global_weeks)
    with col_right:
        games = df_global['game'].loc[(df_global.week==week)]
        game = st.selectbox('On which game do you want to bet?',games)

game_line_in_df = df_global.loc[(df_global.week==week) & ((df_global.game==game))]

home_team = game_line_in_df.iloc[0]['hometeam']
away_team = game_line_in_df.iloc[0]['awayteam']
stadium = game_line_in_df.iloc[0]['stadium']
location = game_line_in_df.iloc[0]['location']

col1, col_team_logo, col_team, col_results, col5 = st.columns(5)

with st.container():  
    with col1:
        st.write(' ')  
    with col_team_logo:
        image = Image.open('src/'+home_team+'.png')
        st.image(image)
        image2 = Image.open('src/'+away_team+'.png')
        st.image(image2)
    with col_team:
        st.markdown("<p style='text-align: center;'>"' '"</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>"' '"</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>"+home_team+"</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>"' '"</p>", unsafe_allow_html=True)
        #st.markdown("<p style='text-align: center;'>"' '"</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>"' '"</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>"+away_team+"</p>", unsafe_allow_html=True)
    with col_results:
        #st.balloons()
        st.markdown("<p style='text-align: center;'>"' '"</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>"' '"</p>", unsafe_allow_html=True)
        if(game_line_in_df.iloc[0]['winner']==1):
                st.markdown("<p style='text-align: center;'>"'Winner! 🏆'"</p>", unsafe_allow_html=True)
        else: st.markdown("<p style='text-align: center;'>"' '"</p>", unsafe_allow_html=True) 
        st.markdown("<p style='text-align: center;'>"' '"</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>"' '"</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>"' '"</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>"' '"</p>", unsafe_allow_html=True)
        if(game_line_in_df.iloc[0]['winner']==0):
                st.markdown("<p style='text-align: center;'>"'Winner! 🏆'"</p>", unsafe_allow_html=True)
        else: st.markdown("<p style='text-align: center;'>"' '"</p>", unsafe_allow_html=True) 
    with col5:
        st.write(' ')

#if(game_line_in_df.iloc[0]['winner']==1):
    #confidence_level = (round(game_line_in_df.iloc[0]['proba_home'], 2))
#else: confidence_level = (round(game_line_in_df.iloc[0]['proba_away'], 2))

with st.container():
    st.markdown("<p style='text-align: center;'>"'In which stadium will the game take place? '+stadium+"</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>"'In which city will the game take place? '+location+"</p>", unsafe_allow_html=True)

st.text('')
st.text('')

# Some metrics under the prediction

#home_average_win_2021 = 
#away_average_win_2021 = 

#home_average_win_2020 = 
#away_average_win_2020 = 

#col0, col1, col2, col3, col4 = st.columns(5)
#col1.metric("Temperature", "70 °F", "1.2 °F")
#col2.metric("Wind", "9 mph", "-8%")
#col3.metric("Confidence level", confidence_level, "🤞")


### CALENDAR OF THE SEASON

with st.container():
        global_weeks = st.selectbox('Select a week to have the summary of our predictions', weeks)


games = df.loc[(df.week==global_weeks)]
games.reset_index()

df_global = pd.read_csv('results_games_2022_xgb.csv')
df_global = df_global.loc[(df_global.week==global_weeks)]
df_global = df_global.replace("Commanders", "Washington")
df_global.reset_index()

col1 , col_home_team , col_away_team, col_winner , col5 = st.columns(5)

with st.container():
    with col1:
        st.write(' ')
    with col_home_team:
        new_title = '<p style="font-family:sans-serif; color:Black; font-size: 14px;">Home Team 🏠</p>'
        st.caption(new_title, unsafe_allow_html=True)
    with col_away_team:
        new_title = '<p style="font-family:sans-serif; color:Black; font-size: 14px;">Away Team ✈️</p>'
        st.caption(new_title, unsafe_allow_html=True)
    with col_winner:
        new_title = '<p style="font-family:sans-serif; color:Blue; font-size: 14px;"><b>Winner 🏆</b></p>'
        st.caption(new_title, unsafe_allow_html=True)
    with col5:
        st.write(' ')

for index,row in df_global.iterrows():
    with st.container():
        with col1:
            st.write(' ')
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
        with col5:
            st.write(' ')



   