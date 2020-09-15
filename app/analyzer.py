import re

from nltk import PorterStemmer
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
import scraper
import requests
import json
from flask import jsonify, Flask
from urllib.request import Request, urlopen
from urllib.parse import urlencode

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}
url = 'https://project-alfa.herokuapp.com/articles'
s = requests.get(url)
print(s)
data = s.json()
suggestions = []
solutions = []
articles = []
results = []
for i in data:
    #print(i['suggestions'][0]5)
    articles.append(i)
    suggestions.append(i['suggestions'][0]['description'])

def predict(log_entry):
    print("Log entry: " + log_entry)
    log_entry = re.sub(
        r"\[[(\w+\d+\s+:\.)]+|\]|/(\w+/)+|(http(://(\w+\.)+))+|(https(://(\w+\.)+))+|(\([\w+\.|\w+,|\w+\)|\w+\\|\.]+)|line(\s+\d+)|referer(:\w+)+|[^a-zA-Z\s+]|\d+|\w+(\-|_|\w+)*\.php|AH|referer|COS|za",
        " ", log_entry)
    unstemmed_log_entry = log_entry
    log_entry = log_entry.split()
    ps = PorterStemmer()
    log_entry = [ps.stem(word) for word in log_entry]
    word_list = []
    solution_list = []

    # solutions = [
    #     'Fatal error: Call to undefined function mysqli() in',
    #     'Apache Error: No matching DirectoryIndex',
    #     'configuring apache2 - LDAP and understanding LDAP configuration',
    #     'Apache2 LDAP subgroup check',
    #     'PHP - Failed to open stream : No such file or directory',
    #     'Notice: Undefined index: variable',
    #     'Fatal error: Call to undefined function mysqli() in',
    #     'PHP Notice: Undefined index: [duplicate]',
    #     'Access denied for user  (using password: YES) except root user'
    # ]

    original_solutions = suggestions
    solutions_temp = []
    solutions = [line.split() for line in suggestions ]
    for line in solutions:
        line = [ps.stem(word) for word in line]
        solutions_temp.append(line)
    solutions = solutions_temp

    for solution in solutions:
        s_list = []
        for s in solution:
            temp_syn = wn.synsets(str(s), pos=wn.NOUN)
            syn = temp_syn[0] if len(temp_syn) > 0 else None
            if syn is not None:
                s_list.append(syn)
        solution_list.append(s_list)

    for word in log_entry:
        temp_syn = wn.synsets(str(word), pos=wn.NOUN)
        syn = temp_syn[0] if len(temp_syn) > 0 else None
        if syn is not None:
            word_list.append(syn)
    brown_ic = wordnet_ic.ic('ic-brown.dat')
    similarity = 0
    similarities = []
    count = 0
    for i in solution_list:
        if len(i) == 0:
            i.append(wn.synsets('apple', pos=wn.NOUN)[0])
    for i in solution_list:
        for j in i:
            for k in word_list:
                s = k.res_similarity(j, brown_ic)
                similarity += s
        similarities.append(similarity)
        similarity = 0
        count += 1
    print(str(max(similarities)) + '\t' + articles[similarities.index(max(similarities))]['suggestions'][0]['description'])
    if max(similarities) < 160:
        print('Scraping')
        descr, link =  scraper.scrape(unstemmed_log_entry)
        payload = json.dumps({"link": link, "description": descr})
        add = requests.post(url, json = {"link": link, "description": descr} , headers  = headers)
        print(add.content)
        results.append({"link": link, "description": descr})
    else:
        result_article = articles[similarities.index(max(similarities))]['suggestions'][0]
        description = result_article['description']
        link = result_article['link']
        results.append({"link": link, "description": description})


def fetch_result(entries):
    # with open('data/log files/test.log') as fp:
    #     for line in fp:
    #         print(line)
    #         print(predict(line))
    #         print(results)
    #         print('=================================================')
    for i in entries:
        print(i)
        predict(i)
    return jsonify(results)


