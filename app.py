from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)
client= MongoClient('localhost', 27017)
db = client.veterinaria
insertDate_collection= db.insertDate   ##creando la coleccion

@app.route("/")
def hello():
    return "HELLO WORLD!"

@app.route("/registrarMascota/", methods= ["GET", "POST"])
def vistaFormRegistro():
    if request.method == 'POST':
        petName= request.form['petName']
        datePet= request.form['datePet']
        race= request.form['race']
        ownerName= request.form['ownerName']
        ownerDni= request.form['ownerDni']
    return render_template("registrar.html")
    # return "Se han registrado los datos"

# @app.route("/registrar", methods=['POST'])
# def registrar():
#     petName= request.form['petName']
#     datePet= request.form['datePet']
#     race= request.form['race']
#     ownerName= request.form['ownerName']
#     ownerDni= request.form['ownerDni']
#     insertDate_collection.insert_one({'petName': petName, 'datePet': datePet, 'race': race, 'ownerName': ownerName, 'ownerDni': ownerDni})
#     return "Se ha registrado la mascota"
#     # insertDate= insertDate_collection.find()
#     # return render_template('registrar.html', insertDate= insertDate)


    



