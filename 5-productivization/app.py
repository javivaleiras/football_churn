# -*- coding: utf-8 -*-


import flask
from flask import Flask, jsonify, request
import json
import pickle
import numpy as np


def load_models():
    file_name = "models/model_file.p"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model


app = Flask(__name__)

@app.route('/predict', methods=['GET'])

def predict():
    # stub input features
    data = request.get_json() 
    # load model
    print("ssssssssssssssssssssssssssssssss")
    model = load_models()
    prediction = model.predict(np.array(list(data.values())))
    response = json.dumps({'response': prediction[0]})
    
    return response, 200


if __name__ == '__main__':
    application.run(debug=True)