from flask import Flask
from flask_pymongo import pymongo
from app import app

DB_CONNECTION= "mongodb://pyraspace:pyraspace2020@learning-shard-00-00-jaac5.mongodb.net:27017,learning-shard-00-01-jaac5.mongodb.net:27017,learning-shard-00-02-jaac5.mongodb.net:27017/ALFA_DB?ssl=true&replicaSet=learning-shard-0&authSource=admin&retryWrites=true&w=majority"

client = pymongo.MongoClient(DB_CONNECTION)
db = client.get_database('ALFA_DB')
user_collection = pymongo.collection.Collection(db, 'kb_articles')