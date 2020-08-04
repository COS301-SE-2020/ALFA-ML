# Dependencies
from flask import Flask, request, jsonify
import pandas as pd
import numpy as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import re
import nltk
from nltk.stem.porter import PorterStemmer
import db

# load model
model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
# API definition
app = Flask(__name__)

# Middleware

# This is the function that uses the trained ML model to predict the correct knowledgebase article
# @return an index number
def predict():
    # get data
    data = request.get_json(force=True)
    log_entry = data['entry']

    # text preprocessing phase
    # convert data to a form that can be read by the model
    corpus = []
    log_entry = re.sub(r"\[[(\w+\d+\s+:\.)]+|\]|/(\w+/)+|(http(://(\w+\.)+))+|(https(://(\w+\.)+))+|(\([\w+\.|\w+,|\w+\)|\w+\\|\.]+)|line(\s+\d+)|referer(:\w+)+|[^a-zA-Z\s+]|\d+|\w+(\-|_|\w+)*\.php|AH|referer|COS|za", " ", log_entry)
    log_entry = log_entry.split()
    ps = PorterStemmer()
    log_entry = [ps.stem(word) for word in log_entry]
    log_entry = ' '.join(log_entry)
    corpus.append(log_entry)
    X = vectorizer.transform(corpus).toarray()

    # make the prediction
    y_pred = model.predict(X)
    
    # assign the predicted number as a knowledgebase article
    kb_index = y_pred[0]

    # return data
    return int(kb_index)

# This function uses the index number to fetch the corresponding knowledgebase article from the database
# @return data from database as json object
def fetch_data(index):
    queryObject = {'kb_index': index}
    res = db.db.kb_articles.find_one(queryObject) 
    res.pop('_id')
    res.pop('kb_index')
    return jsonify(res)

# routes
@app.route("/")
def home():
	msg = {"message": "API is running"}
	return jsonify(msg)

@app.route("/analyse", methods=['POST'])
def analyse():
    index = predict()
    result = fetch_data(index)
    return result

if __name__ == '__main__':
    app.run(port=6667, debug=True)