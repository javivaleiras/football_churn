# -*- coding: utf-8 -*-

import requests
from input_data import data_input,transfrom_data_in

URL = 'http://127.0.0.1:5000/predict'
headers = {"Content-Type": "application/json"}

data = {"input": transfrom_data_in(data_input)}

r = requests.get(URL,headers=headers, json=data) 

r.json()