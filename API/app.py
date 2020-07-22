# Dependencies
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import re
import nltk
from nltk.stem.porter import PorterStemmer

# load model
model = pickle.load(open('model.pkl', 'rb'))

# API definition
app = Flask(__name__)

# routes
@app.route("/predict", methods=['POST'])
def predict():
    # get data
    data = request.get_json(force=True)
    print("Original: ", data)
    log_entry = data['entry']
    print("Value: ", log_entry)

    # convert data to 2d matrix
    corpus = []
    log_entry = re.sub(r"\[[(\w+\d+\s+:\.)]+|\]|/(\w+/)+|(http(://(\w+\.)+))+|(https(://(\w+\.)+))+|(\([\w+\.|\w+,|\w+\)|\w+\\|\.]+)|line(\s+\d+)|referer(:\w+)+|[^a-zA-Z\s+]|\d+|\w+(\-|_|\w+)*\.php|AH|referer|COS|za", " ", log_entry)
    log_entry = log_entry.split()
    ps = PorterStemmer()
    log_entry = [ps.stem(word) for word in log_entry]
    log_entry = ' '.join(log_entry)
    #print("Corpus what what: ", log_entry)

    corpus.append(log_entry)
    print("Corpus what what:", corpus)
    countVectorizer = CountVectorizer(max_features = 1500)
    X = countVectorizer.fit_transform(corpus).toarray()
    np

    y_pred = model.predict(X)
    print("Prediction please God: ", y_pred)
    
    # send back to client
    output = {'prediction': int(y_pred[0]) }

    # return data
    return jsonify(results=output)

if __name__ == '__main__':
    app.run(port=6667, debug=True)