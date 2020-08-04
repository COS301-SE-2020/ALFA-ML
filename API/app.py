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
# load the vectorizer; Bag-of-Words vector
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
# API definition
app = Flask(__name__)

# MIDDLEWARE

# This is the function that uses the trained ML model to predict the correct knowledgebase article
# @return a list of indexes to the knowledgebase articles
def predict():
    # get data
    log_file = request.files["log_file"]

    # Split the string with respect to the new line operator "\n" to separate the individual log file entries
    log_file_entries = log_file.getvalue().splitlines()

    # remove duplicates
    log_file_entries = list(dict.fromkeys(log_file_entries))

    # text preprocessing phase
    # convert data to a form that can be read by the model
    corpus = []
    for log_entry in log_file_entries:
        log_entry = str(log_entry)
        log_entry = re.sub(r"\[[(\w+\d+\s+:\.)]+|\]|/(\w+/)+|(http(://(\w+\.)+))+|(https(://(\w+\.)+))+|(\([\w+\.|\w+,|\w+\)|\w+\\|\.]+)|line(\s+\d+)|referer(:\w+)+|[^a-zA-Z\s+]|\d+|\w+(\-|_|\w+)*\.php|AH|referer|COS|za|b", " ", log_entry)
        log_entry = log_entry.split()
        ps = PorterStemmer()
        log_entry = [ps.stem(word) for word in log_entry]
        log_entry = ' '.join(log_entry)
        corpus.append(log_entry)
    
    # Use Bag-of-Words word embedding to transform text into numbers that can be read by model
    X = vectorizer.transform(corpus).toarray()

    # make the prediction
    kb_indexes = model.predict(X)

    # return data
    data = {
        'log_file_entries': log_file_entries, 
        'kb_indexes': kb_indexes
    }
    return data

# This function uses the index number to fetch the corresponding knowledgebase article from the database
# @return data consisting of the errors encountered and their corresponding knowledgebase articles
def fetch_data(data):
    kb_indexes = data['kb_indexes']
    suggested_solutions = []

    for index in kb_indexes:
        queryObject = {'kb_index': int(index)}
        res = db.db.kb_articles.find_one(queryObject)
        res.pop('_id')
        res.pop('kb_index')
        suggested_solutions.append(res)

    results = {
        'log_file_entries': data['log_file_entries'],
        'suggested_solutions': suggested_solutions
    }

    return jsonify(results)

# routes
@app.route("/")
def home():
	msg = {"message": "API is running"}
	return jsonify(msg)

@app.route("/analyse", methods=['POST'])
def analyse():
    indexes = predict()
    results = fetch_data(indexes)
    return results

if __name__ == '__main__':
    app.run(port=6667, debug=True)