from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from forms import RegistrandoM
from flask_wtf import CSRFProtect
from datetime import datetime
from config import Config



app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect()
client= MongoClient('localhost', 27017)
db = client.veterinaria
insertDate_collection= db.insertDate   ##creando la coleccion
date= datetime


@app.route("/")
def hello():
    return "HELLO WORLD!"

@app.route("/inicio")
def inicio():
    return "Mascota registrada!"


@app.route("/registrarMascota/", methods= ["GET", "POST"])
def vistaFormRegistro():
    form = RegistrandoM()
    if form.validate_on_submit():
        petName= form.petName.data
        datePet= form.datePet.data
        race= form.race.data
        ownerName= form.ownerName.data
        ownerDni= form.ownerDni.data
    
    if request.method== 'POST':
        petName= form.petName.data
        datePet= form.datePet.data
        race= form.race.data
        ownerName= form.ownerName.data
        ownerDni= form.ownerDni.data
        insertDate_collection.insert_one({'petName': petName, 'datePet': datePet, 'race': race, 'ownerName': ownerName, 'ownerDni': ownerDni})

        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('inicio'))
    return render_template("registrar.html", form= form)





    



