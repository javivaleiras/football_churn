# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 22:27:43 2023

@author: javic
"""
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler

data_input = [
    "Spezia",
    26,
    "D(R)",
    2,
    85,
    0,
    0,
    0,
    0,
    0,
    85.4,
    0.5,
    0,
    5.86,
    0.5,
    0.5,
    0,
    0,
    0.5,
    1.5,
    0,
    0,
    0,
    0,
    0,
    0.5,
    0,
    1,
    20.5,
    0,
    1,
    0,
    "Serie A"
    ]



def transfrom_data_in(data):
    df = create_df(data)
    df = feature_engineering(df)
    df = encode_categoricals(df)
    df = scale_features(df)
    
    return df.tolist()
    

def scale_features(df):
    scaler= joblib.load('scalers/scaler.joblib')
    scaled_df = scaler.transform(df)
    
    return scaled_df
    
def encode_categoricals(df):
    # load encoders
    onehot_encoder_club = joblib.load('encoders/encoder_club.joblib')
    onehot_encoder_apps = joblib.load('encoders/encoder_apps.joblib')
    onehot_encoder_league = joblib.load('encoders/encoder_league.joblib')
    onehot_encoder_pos = joblib.load('encoders/encoder_position.joblib')
    
    # create dfs with encoded data
    clubs_df = pd.DataFrame(onehot_encoder_club.transform(df[['club']]).toarray() , 
                        columns=onehot_encoder_club.get_feature_names_out(['club']))

    pos_df = pd.DataFrame(onehot_encoder_pos.transform(df[['position']]).toarray(),
                        columns=onehot_encoder_pos.get_feature_names_out(['position']))

    league_df = pd.DataFrame(onehot_encoder_league.transform(df[['league']]).toarray(),
                        columns=onehot_encoder_league.get_feature_names_out(['league']))

    apps_df = pd.DataFrame(onehot_encoder_apps.transform(df[['apps_cat']]).toarray(),
                        columns=onehot_encoder_apps.get_feature_names_out(['apps_cat']))
    
    # add variable to df
    df = df.join(clubs_df)
    df = df.join(pos_df)
    df = df.join(league_df)
    df = df.join(apps_df)
    
    # drop old features
    df = df.drop(['club','position','league','apps_cat'],axis=1)
    
    return df

def feature_engineering(df):
    
    # create weighted features
    total_games = df['apps'].max()
    to_w = ['shots','yel','red','aerials_won',
       'tackles', 'interceptions', 'fouls', 'offsides_won', 'clearances',
       'dribbled', 'blocks', 'own_goals', 'key_passes', 'dribblings', 'fouled',
       'offsides', 'dispossed', 'bad_controls', 'avg_passes', 'crosses',
       'long_passes', 'through_passes']
    
    for x in to_w:
        df["w_"+x] = (df[x] * df['apps']) / total_games
    
    #create special weighted ps%
    avg_max_avg_passes = df.groupby("league")['avg_passes'].max().mean()
    df['w_ps_avg_passes'] = (df['avg_passes'] * (df['ps%'] )) / avg_max_avg_passes
    
    # remove original features
    df = df.drop(to_w,axis=1)
    df = df.drop('ps%',axis=1)
    
    # categorize apps
    df['apps_cat'] = pd.qcut(df['apps'], q=1)
    df = df.drop('apps',axis=1)
    
    return df
    
def create_df(data):
    df = pd.DataFrame([data],columns=['club','age','position','apps',
                                       'mins','goals','assists','yel',
                                       'red','shots','ps%','aerials_won',
                                       'motm','rating','tackles','interceptions',
                                       'fouls','offsides_won','clearances',
                                       'dribbled','blocks','own_goals',
                                       'key_passes','dribblings','fouled',
                                       'offsides','dispossed','bad_controls',
                                       'avg_passes','crosses','long_passes',
                                       'through_passes','league'])
    return df
    