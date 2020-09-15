from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import urllib.parse
import requests

def scrape(query):
    query = urllib.parse.quote(query)
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    headers = {'User-Agent': user_agent}
    url = 'http://www.google.com/search?q=' + query
    print(url)
    # req = Request(url)
    # req.add_header('User-Agent', user_agent)
    # page = urlopen(req).read().decode('utf-8')
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    # print(soup.find("div", {"class": "r"}).a['href'])
    new_url = soup.find("div", {"class": "r"}).a['href']
    print(new_url)
    page = requests.get(new_url, headers = headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    # print(soup.title.string)
    return (soup.title.string, new_url)
