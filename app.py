from flask import Flask, render_template, request, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)
client= MongoClient('localhost', 27017)
db = client.veterinaria
insertDate_collection= db.insertDate   ##creando la coleccion

@app.route("/")
def hello_world():
    return "<h1>Hola, mundo!</h1>"

@app.route("/registrar", methods=['POST'])
def registrar():
    petName= request.form['petName']
    datePet= request.form['datePet']
    race= request.form['race']
    ownerName= request.form['ownerName']
    ownerDni= request.form['ownerDni']
    insertDate_collection.insert_one({'petName': petName, 'datePet': datePet, 'race': race, 'ownerName': ownerName, 'ownerDni': ownerDni})
    insertDate= insertDate_collection.find()
    return render_template('registrar.html', insertDate= insertDate)

    



