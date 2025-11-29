from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'clave-secreta')

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://peliculas:peliculasi267@peliculas.0nwsmz.mongodb.net/peliculasi267?retryWrites=true&w=majority')
client = MongoClient(MONGO_URI)
db = client.peliculasi267
collection = db.peliculas

def to_str_id(doc):
    if doc and '_id' in doc:
        doc['id'] = str(doc['_id'])
    return doc

def to_str_list(cursor):
    return [to_str_id(d) for d in cursor]

@app.route('/')
def index():
    peliculas = to_str_list(collection.find())
    return render_template('index.html', peliculas=peliculas)

if __name__ == '__main__':
    app.run(debug=True)
