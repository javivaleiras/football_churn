# -*- coding: utf-8 -*-


import flask
from flask import Flask, jsonify, request
import json
import pickle

app = Flask(__name__)

@app.route('/predict', methods=['GET'])

def load_models():
    file_name = "models/model_file.p"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model

def predict():
    # stub input features
    x = 5.963    
    # load model
    model = load_models()
    prediction = model.predict([[x]])[0]
    response = json.dumps({'response': prediction})
    return response, 200


if __name__ == '__main__':
    application.run(debug=True)