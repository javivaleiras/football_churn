# -*- coding: utf-8 -*-


import flask
from flask import Flask, jsonify, request
import json
import pickle
import numpy as np
import joblib

def load_models():
    file_name = 'models/random_forest.joblib'
    
    model = joblib.load(file_name)
    return model
    # file_name = "models/random_forest.pkl"
    # with open(file_name, 'rb') as pickled:
    #     data = pickle.load(pickled)
    #     model = data['model']
    # return model


app = Flask(__name__)

@app.route('/predict', methods=['GET'])

def predict():
    request_json = request.get_json()
    x = request_json['input']
    
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