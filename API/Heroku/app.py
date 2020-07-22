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

# API definition
app = Flask(__name__)

# Middleware
def predict():
    # get data
    data = request.get_json(force=True)
    print("Original: ", data)
    log_entry = data['entry']
    #print("Value: ", log_entry)

    # convert data to 2d matrix
    corpus = []
    log_entry = re.sub(r"\[[(\w+\d+\s+:\.)]+|\]|/(\w+/)+|(http(://(\w+\.)+))+|(https(://(\w+\.)+))+|(\([\w+\.|\w+,|\w+\)|\w+\\|\.]+)|line(\s+\d+)|referer(:\w+)+|[^a-zA-Z\s+]|\d+|\w+(\-|_|\w+)*\.php|AH|referer|COS|za", " ", log_entry)
    log_entry = log_entry.split()
    ps = PorterStemmer()
    log_entry = [ps.stem(word) for word in log_entry]
    log_entry = ' '.join(log_entry)
    #print("Corpus what what: ", log_entry)

    corpus.append(log_entry)
    #print("Corpus what what:", corpus)
    countVectorizer = CountVectorizer(max_features = 1500)
    X = countVectorizer.fit_transform(corpus).toarray()
    
    X = X.transpose()

    y_pred = model.predict(X)
    
    kb_index = y_pred[0]
    #print("index", y_pred[0])
    #print("Prediction please God: ", y_pred)

    # send back to client
    #output = {'prediction': int(y_pred[0]) }

    # return data
    #return jsonify(results=output)
    return int(kb_index)

def fetch_data(index):
    #db.db.kb_articles.insert_one({"name": "John"})
    queryObject = {'kb_index': index}
    res = db.db.kb_articles.find_one(queryObject) 
    res.pop('_id')
    res.pop('kb_index')
    return jsonify(res)

# routes
@app.route("/predict", methods=['POST'])
def analyze():
    index = predict()
    result = fetch_data(index)
    #result['status'] = "success"
    return result

if __name__ == '__main__':
    app.run(port=6667, debug=True)