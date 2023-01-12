# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 23:41:50 2023

@author: javic
"""

import flask
from flask import Flask, jsonify, request
import json
import pickle
import numpy as np
import joblib
from transformations import transform_data_in


# load the random forest model
def load_models():
    file_name = 'models/random_forest.joblib'
    
    model = joblib.load(file_name)
    return model

app = Flask(__name__)

@app.route('/predict', methods=['GET'])

def predict():
    request_json = request.get_json()
    # get the data input
    x = request_json['input'] 
    # transforms data according to model input
    x = transform_data_in(x)    
    # load model
    model = load_models()
    prediction = model.predict(x)
    if prediction == 1:
        answer = "yes, the player will leave the team"
    else:
        answer = "no, the player will not leave the team"
    response = json.dumps({'response': answer})
    return response, 200


if __name__ == '__main__':
    application.run(debug=True)