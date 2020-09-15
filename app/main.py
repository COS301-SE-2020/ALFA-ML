# Dependencies
from flask import Flask, request, jsonify
import pandas as pd
import numpy as pd
from sklearn.feature_extraction.text import CountVectorizer
import re
import nltk
from nltk.stem.porter import PorterStemmer
import base64
import pybase64
from flask import Flask
from flask_pymongo import pymongo
from datetime import date, datetime
#from flask_cors import CORS, cross_origin
from . import analyzer
DB_CONNECTION="mongodb://pyraspace:pyraspace2020@learning-shard-00-00-jaac5.mongodb.net:27017,learning-shard-00-01-jaac5.mongodb.net:27017,learning-shard-00-02-jaac5.mongodb.net:27017/ALFA_DB?ssl=true&replicaSet=learning-shard-0&authSource=admin&retryWrites=true&w=majority"

client = pymongo.MongoClient(DB_CONNECTION)
db = client.get_database('ALFA_DB')
user_collection = pymongo.collection.Collection(db, 'kb_articles')
user_collection1 = pymongo.collection.Collection(db, 'log_files')
user_collection2 = pymongo.collection.Collection(db, 'analysis_history')


# API definition
app = Flask(__name__)

# Fix CORS errorsCORS(app, support_credentials=True)

# MIDDLEWARE

def store_analysis_data(solution_results):
	analysis_to_be_saved = {
		"save_date": str(date.today()),
		"save_time": str(datetime.now().strftime("%H:%M:%S")),
		"analysis_data": solution_results
	}
	db.analysis_history.insert_one(analysis_to_be_saved)


def store_log_file(log_file_contents, log_file_filename):
	log_file_to_be_saved = {
    	"upload_date": str(date.today()),
    	"upload_time": str(datetime.now().strftime("%H:%M:%S")),
    	"filename": log_file_filename,
    	"contents": log_file_contents
    }
	db.log_files.insert_one(log_file_to_be_saved)


# This is the function that uses the trained ML model to predict the correct knowledgebase article
# @return a list of indexes to the knowledgebase articles
def predict():

    # get data
    # decode base64 file
    print('Hello')
    log_file = pybase64.b64decode(request.get_json(force=True)['content']).decode('ascii').splitlines()

    log_filename = request.get_json(force=True)['filename']

    # # create log file input to save to database
    # store_log_file(log_file, log_filename)
    #
    # # Split the string with respect to the newline operator "\n" to separate the individual log file entries
    # log_file = request.get_json(force=True)['content']
    # raw_log_file_entries = log_file.splitlines()
    #
    # # add line numbers to each log file entry
    # line = 1
    # metadata = {}
    log_file_entries_metadata = []
    # for entry in range(len(raw_log_file_entries)):
    #     metadata = { "line_no": line,
    #                 "log_entry": raw_log_file_entries[entry] }
    #     log_file_entries_metadata.append(metadata)
    #     line += 1
    #print(log_file_entries_metadata)

    # remove duplicates
    # tracker = []
    # log_file_entries = []
    # for i in range(len(raw_log_file_entries)):
    #     if raw_log_file_entries[i] not in tracker:
    #         log_file_entries.append(log_file_entries_metadata[i])
    #         tracker.append(raw_log_file_entries[i])
    # print(log_file_entries)
    # logfile = request.get_data()['content']

    return analyzer.fetch_result(log_file)
    #print(log_file_entries)
    #
    # # text preprocessing phase
    # # convert data to a form that can be read by the model
    # corpus = []
    # for entry in log_file_entries:
    #     log_entry = entry['log_entry']
    #     log_entry = str(log_entry)
    #     log_entry = re.sub(r"\[[(\w+\d+\s+:\.)]+|\]|/(\w+/)+|(http(://(\w+\.)+))+|(https(://(\w+\.)+))+|(\([\w+\.|\w+,|\w+\)|\w+\\|\.]+)|line(\s+\d+)|referer(:\w+)+|[^a-zA-Z\s+]|\d+|\w+(\-|_|\w+)*\.php|AH|referer|COS|za|b", " ", log_entry)
    #     log_entry = log_entry.split()
    #     ps = PorterStemmer()
    #     log_entry = [ps.stem(word) for word in log_entry]
    #     log_entry = ' '.join(log_entry)
    #     corpus.append(log_entry)
    #
    # # Use Bag-of-Words word embedding to transform text into numbers that can be read by model
    # input_data = vectorizer.transform(corpus).toarray()
    #
    # # make the prediction
    # kb_indexes = model.predict(input_data)
    #
    # # return data
    # data = {
    #     'log_file_entries': log_file_entries,
    #     'kb_indexes': kb_indexes
    # }
    #
    # # return data
    # return data
    
# This function uses the index number to fetch the corresponding knowledgebase article from the database
# @return data consisting of the errors encountered and their corresponding knowledgebase articles
def fetch_data(data):
    kb_indexes = data['kb_indexes']
    solution_results = []

    for i in range(len(kb_indexes)):
        queryObject = {'kb_index': int(i)} # where we query the object
        res = db.kb_articles.find_one(queryObject)
        res.pop('_id') # _id of the entire document entry
        res.pop('__v')
        res['line_no'] = data['log_file_entries'][i]['line_no']
        res['log_entry'] = data['log_file_entries'][i]['log_entry']
        solution_results.append(res)

    # convert ObjectId so it can be JSON serialized
    for sol in solution_results:
    	for sug in sol['suggestions']:
    		sug['_id'] = str(sug['_id'])

    # shorten the results because they don't yet fit into the UI
    shortened_result = []
    for i in range(4):
    	shortened_result.append(solution_results[i])

    # save the log file analysis data to be viewed as history
    store_analysis_data(shortened_result)

    return jsonify(shortened_result)
    

# routes
@app.route("/")
def home():
	msg = {"message": "API is running"}
	return jsonify(msg)

@app.route("/analyse", methods=['POST'])
@cross_origin(supports_credentials=True)
def analyse():
    #indexes = predict()
    return predict()
    

if __name__ == '__main__':
    app.run()
