# Dependencies
from flask import Flask, request, jsonify
from sklearn.externals import joblib
import traceback
import pandas as pd
import numpy as np

# API definition
app = Flask(__name__)

@app.route("/predict", methods=['POST'])
def predict():
    json_ = request.json
    print(json_)
    query = pd.get_dummies(pd.DataFrame(json_))
    print("here: ", query)
    prediction = list(nb_classifier.predict(query))
    print("here is the prediction", prediction)
    return jsonify({ 'prediction': prediction })


if __name__ == '__main__':
    try:
        port = int(sys.argv[1]) # This is for a command-line input
    except:
        port = 12345 # If you don't provide any port the port will be set to 12345

    nb_classifier = joblib.load("naive-bayes-model.pkl") # Load "nb-model.pkl"
    print ('Model loaded')

    app.run(port=port, debug=True)