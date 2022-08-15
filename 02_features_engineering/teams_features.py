import json
import pandas as pd
import os
import numpy as np
import boto3
from botocore.client import Config as BotoConfig

s3 = boto3.client('s3',aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
s3_obj = s3.get_object(Bucket='nflpredictor-scrapy', Key='espn_scores.json')
json_data = s3_obj["Body"].read().decode('utf-8')
data = json.loads(json_data)
#with open('../01_scraping/json/espn_scores.json') as rosters:
#    data = json.load(rosters)

df = pd.json_normalize(data)
#print(df)

df.drop(['boxscore', 'gamecast',"awayteam global record","awayteam away record","hometeam global record","hometeam home record"], axis=1, inplace=True)
df.reset_index()

#df = df.loc[((df.awayteam=='Texans') | (df.hometeam=='Texans')) & (df.season=='2020')]
#from calendar import week


df.week = df.week.astype(int)
df.awayscore = df.awayscore.astype(int)
df.homescore = df.homescore.astype(int)
df.season = df.season.astype(int)
df = df.sort_values(by=['season', 'week'],ascending = [True, True])
#   - Addition of analysis features:

#df.insert(df.shape[1],"score_abs",df["homescore"] - df["awayscore"]) #Absolute score of the game
df = df.assign(scoreabs=df.awayscore-df.homescore)
df = df.assign(winner=df.hometeam)
df= df.assign(loser=df.awayteam)
df.winner = df[['awayteam','hometeam','scoreabs']].apply(lambda x: x['awayteam'] if x['scoreabs']>0 else x['hometeam'], axis=1)
df.loser = df[['awayteam','hometeam','scoreabs']].apply(lambda x: x['awayteam'] if x['scoreabs']<0 else x['hometeam'], axis=1)

#df = df.assign(streak_home=0)
#df = df.assign(streak_away=0)
#df.streak_home = df[['awayteam','hometeam','winner']].apply(lambda x: 1 if x['hometeam']==x['winner'] else 0, axis=1)
#df.streak_away = df[['awayteam','hometeam','winner']].apply(lambda x: 1 if x['awayteam']==x['winner'] else 0, axis=1)

df_teams_stats_away = pd.DataFrame().assign(season=df.season, week=df.week, idgame=df.idgame, team=df.awayteam, winner=df.winner, loser=df.loser)
df_teams_stats_home = pd.DataFrame().assign(season=df.season, week=df.week, idgame=df.idgame, team=df.hometeam, winner=df.winner, loser=df.loser)

#df_teams_stats.append({'season' : df.season, 'week' : df.week, 'idgame' : df.idgame, 'team' : df.hometeam, 'winner' : df.winner},ignore_index=True)

def f(x):
    #x['streak'] = x.groupby( (x['loser']!=x['team']).cumsum()).cumcount()+( (x['team'] != x['loser']).cumsum() == 0).astype(int) 
    x['c'] = (x['loser'] == x['team']).cumsum()
    x['a'] = (x['c'] == 0).astype(int)
    x['b'] = x.groupby('c').cumcount()
    x['win_streak'] = x.groupby('c').cumcount()+x['a']
    x.drop(['a', 'b', 'c'], axis=1, inplace=True)
    return x

def g(x):
#x['streak'] = x.groupby( (x['loser']!=x['team']).cumsum()).cumcount()+( (x['team'] != x['loser']).cumsum() == 0).astype(int) 
    x['c'] = (x['winner'] == x['team']).cumsum()
    x['a'] = (x['c'] == 0).astype(int)
    x['b'] = x.groupby('c').cumcount()
    x['lose_streak'] = x.groupby('c').cumcount()+x['a']
    x.drop(['a', 'b', 'c'], axis=1, inplace=True)
    return x

#d.concat([new_df,entry])
df_teams_stats = pd.concat([df_teams_stats_away,df_teams_stats_home], ignore_index=True, sort=False)
df_teams_stats = df_teams_stats.sort_values(by=['season','team','week'],ascending=[True,True,True])
df_teams_stats = df_teams_stats.reset_index(drop=True,inplace=False)
#df_teams_stats = df_teams_stats.assign(streak_before=0)
df_teams_stats = df_teams_stats.assign(win_streak=0)
df_teams_stats = df_teams_stats.assign(lose_streak=0)
#df_teams_stats.streak_before = df_teams_stats[['team','winner','week']].apply(lambda x: 0 if (x['week']==1) else -1, axis=1)
#df_teams_stats.streak_after = df_teams_stats[['team','winner','week']].apply(lambda x: 1 if (x['week']==1 & (x['winner']==x['team'])) else -1, axis=1)
df_teams_stats = df_teams_stats.groupby('team', sort=False).apply(f)
df_teams_stats = df_teams_stats.groupby('team', sort=False).apply(g)
#df_teams_stats = df_teams_stats.loc[df_teams_stats.team=='Jets']
#df_teams_stats = df_teams_stats.loc[df_teams_stats.season==2017]
print(df_teams_stats)



#df_teams_stats = df_teams_stats.sort_values(by=['season','week','idgame'],ascending=[True,True,True])
#df_teams_stats = df_teams_stats.reset_index(drop=True,inplace=True)
#df_teams_stats
#df_teams_stats = df.assign(streak=0)
#df_teams_stats.streak = df_teams_stats[['team','winner','week']].apply(lambda x: 1 if (x['team']==x['winner']) else 0, axis=1)
#df_team_stats = df_teams_stats.groupby(['idgame'])
#series = df.iloc[:,7]
#df['streak'] = df.result.ne(df['winner'].shift())
#df.streak = df[['awayteam','hometeam','scoreabs','week','streak']].apply(lambda x: x['streak']+1 if (x['scoreabs']>0 else x['hometeam'], axis=1)
#df.insert(df.shape[1],"winner_home", 0) #Flagging whether the home team won (1) or lose (0)

#df.loc[:,['streak']] = df.loc[(df.winner & df.week-1)]

#def f(x):
    #x.past_week = x.winner
    #x.streak = x.groupby( (x['stat'] != 0).cumsum()).cumcount()+( (x['stat'] != 0).cumsum() == 0).astype(int) 

#df_teams_stats_home

#df.loc[df.season==2017]
#df.loc[(df.player_name=='Kyler Murray') & (df.game_id==401326597)]