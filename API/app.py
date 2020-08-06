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
import base64

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
    # decode base64 file
    json = request.get_json(force=True)
    log_file = base64.b64decode(json['log'])
    print(log_file)
    
    # Split the string with respect to the newline operator "\n" to separate the individual log file entries
    raw_log_file_entries = log_file.splitlines()

    # add line numbers to each log file entry
    line = 1
    metadata = {}
    log_file_entries_metadata = []
    for entry in range(len(raw_log_file_entries)):
        metadata = { "line_no": line, 
                    "log_entry": raw_log_file_entries[entry] }
        log_file_entries_metadata.append(metadata)
        line += 1
    #print(log_file_entries_metadata)

    # remove duplicates
    tracker = []
    log_file_entries = []
    for i in range(len(raw_log_file_entries)):
        if raw_log_file_entries[i] not in tracker:
            log_file_entries.append(log_file_entries_metadata[i])
            tracker.append(raw_log_file_entries[i])
    
    #print(log_file_entries)

    # text preprocessing phase
    # convert data to a form that can be read by the model
    corpus = []
    for entry in log_file_entries:
        log_entry = entry['log_entry']
        log_entry = str(log_entry)
        log_entry = re.sub(r"\[[(\w+\d+\s+:\.)]+|\]|/(\w+/)+|(http(://(\w+\.)+))+|(https(://(\w+\.)+))+|(\([\w+\.|\w+,|\w+\)|\w+\\|\.]+)|line(\s+\d+)|referer(:\w+)+|[^a-zA-Z\s+]|\d+|\w+(\-|_|\w+)*\.php|AH|referer|COS|za|b", " ", log_entry)
        log_entry = log_entry.split()
        ps = PorterStemmer()
        log_entry = [ps.stem(word) for word in log_entry]
        log_entry = ' '.join(log_entry)
        corpus.append(log_entry)
    
    # Use Bag-of-Words word embedding to transform text into numbers that can be read by model
    input_data = vectorizer.transform(corpus).toarray()

    # make the prediction
    kb_indexes = model.predict(input_data)

    # return data
    data = {
        'log_file_entries': log_file_entries, 
        'kb_indexes': kb_indexes
    }
    # return data
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
    #print(results)
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