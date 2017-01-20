from flask import Flask, jsonify, render_template, request
import cPickle as pickle
from data_point_cleaner import clean_data_point
from pymongo import MongoClient
import requests
import json
from collections import OrderedDict
import numpy as np
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    pass

# Get something from server
@app.route('/hello', methods=['GET'])
def say_hello():
    return "Hello, World!"

@app.route('/score', methods=['GET'])
def score():
    url = "http://galvanize-case-study-on-fraud.herokuapp.com/data_point"
    response = requests.get(url)
    json_data = json.loads(response.text)

    keys = json_data.keys()
    values = np.array(json_data.values())
    values = values[:, np.newaxis].T
    df = pd.DataFrame(columns=keys, data=values)
    # df2 = df[['name', 'country','org_name']]
    df_clean = clean_data_point(df)

    path = 'model.pkl'
    with open(path) as f:
        model_fit = pickle.load(f)

    pred = model_fit.predict(df_clean)[0]

    #pred = 0
    if pred == 0:
        status = "APPROVED"
    else:
        status = "FLAGGED"

    # return jsonify(pred)
    return render_template('app_html.html', status=status, name=df['name'][0], country=df['country'][0], org_name=df['org_name'][0])
    #return jsonify(list(df_clean))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
