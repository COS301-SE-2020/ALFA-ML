# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # NLP Supervised Learning Using Naive Bayes
# %% [markdown]
# ## Importing the libraries

# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# %% [markdown]
# # Importing the dataset

# %%
dataset = pd.read_csv('../data/alfa_dataset.csv - Sheet1.csv', delimiter = ',')
#print(dataset.head())
#print(dataset.shape)

# %% [markdown]
# # Cleaning the text

# %%
import re
import nltk
from nltk.stem.porter import PorterStemmer
corpus = []
for i in range(0, 60):
  #print("here", dataset['Log file entries'][i])
  log_entry = re.sub(r"\[[(\w+\d+\s+:\.)]+|\]|/(\w+/)+|(http(://(\w+\.)+))+|(https(://(\w+\.)+))+|(\([\w+\.|\w+,|\w+\)|\w+\\|\.]+)|line(\s+\d+)|referer(:\w+)+|[^a-zA-Z\s+]|\d+|\w+(\-|_|\w+)*\.php|AH|referer|COS|za", " ", dataset['Log file entries'][i])
  #print(log_entry)
  log_entry = log_entry.split()
  ps = PorterStemmer()
  log_entry = [ps.stem(word) for word in log_entry]
  #print(log_entry)
  log_entry = ' '.join(log_entry)
  #print(log_entry)
  corpus.append(log_entry)

#print(corpus)

# %% [markdown]
# # Creating the Bag of Words Model

# %%
from sklearn.feature_extraction.text import CountVectorizer
countVectorizer = CountVectorizer(max_features = 1500)
X = countVectorizer.fit_transform(corpus).toarray()
y = dataset.iloc[ :, -1].values

# %% [markdown]
# # Splitting the dataset into Training set and Test set

# %%
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# %% [markdown]
# # Training Naive Bayes Model on the Training set

# %%
from sklearn.naive_bayes import GaussianNB
nb_classifier = GaussianNB()
nb_classifier.fit(X_train, y_train)

# %% [markdown]
# # Predicting the test set results

# %%
#y_pred = nb_classifier.predict(X_test)
#print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

#from sklearn.metrics import confusion_matrix, accuracy_score
#cm = confusion_matrix(y_test, y_pred)
#print(cm)
#accuracy_score(y_test, y_pred)


# %%
# Save the model
from sklearn.externals import joblib
joblib.dump(nb_classifier, 'naive-bayes-model.pkl')
print("Model dumped!")


# %%
# Load the model you just saved
nb_classifier = joblib.load('naive-bayes-model.pkl')

