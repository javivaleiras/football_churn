# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 22:27:43 2023

@author: javic
"""

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
    df = pd.DataFrame(data,columns=['club','age','position','apps',
                                    'mins','goals','assists','yel',
                                    'red','shots','ps%','aerials_won',
                                    'motm','rating','tackles','interceptions',
                                    'fouls','offsides_won','clearances',
                                    'dribbled','blocks','own_goals',
                                    'key_passes','dribblings','fouled',
                                    'offsides','dispossed','bad_controls',
                                    'avg_passes','crosses','long_passes',
                                    'through_passes','league'])