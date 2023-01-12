# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 23:44:28 2023

@author: javic
"""

import requests
from input_data import data_input

URL = 'http://127.0.0.1:5000/predict'
headers = {"Content-Type": "application/json"}

data = {"input": data_input}

r = requests.get(URL,headers=headers, json=data) 

r.json()