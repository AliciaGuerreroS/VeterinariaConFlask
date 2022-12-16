from flask import Flask, render_template, request, url_for, redirect, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from forms import RegistrandoM, BuscarMascotE
from flask_wtf import CSRFProtect
from config import Config
import datetime



app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect()
client= MongoClient('localhost', 27017)
db = client.veterinaria
insertDate_collection= db.insertDate   ##creando la coleccion
foudDate_collection= db.foundDate



@app.route("/")
def hello():
    return "HELLO WORLD!"

@app.route("/inicio")
def inicio():
    return "Mascota registrada!"



@app.route("/registrarMascota/", methods= ["GET", "POST"])
def vistaFormRegistro():
    form = RegistrandoM()
    if request.method== 'POST' and form.validate_on_submit():
        petName= form.petName.data
        datePet= form.datePet.data
        time = datetime.datetime.min.time()
        final_date = datetime.datetime.combine(datePet, time)
        race= form.race.data
        ownerName= form.ownerName.data
        ownerDni= form.ownerDni.data
        print(petName, datePet, race, ownerName, ownerDni)
        # # insertDate_collection.insert_one({'petName': petName, 'race': race, 'ownerName': ownerName, 'ownerDni': ownerDni})
        insertDate_collection.insert_one({'petName': petName, 'datePet': final_date, 'race': race, 'ownerName': ownerName, 'ownerDni': ownerDni})

        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('inicio'))
    return render_template("registrar.html", form= form)



@app.route("/buscarMascota/", methods= ['GET', 'POST'])
def buscarMascota():
    global petName
    global ownerDni
    form= BuscarMascotE()
    if request.method == 'POST' and form.validate_on_submit():
        petName= form.petName.data
        ownerDni= form.ownerDni.data
        datos1= insertDate_collection.find({'petName': petName, 'ownerDni': ownerDni})
        print(petName, ownerDni)
        if datos1 == True:
            return redirect(url_for('mostrarMascota'))
        else:
            print('Los resultados no coinciden')
    return render_template('buscarMascota.html', form= form)


@app.route("/mostrarMascota")
def mostrarMascota():
    datos= insertDate_collection.find({'petName': petName, 'ownerDni': ownerDni})
    return render_template("mostrarMascota.html", datos= datos)
    

#https://www.youtube.com/watch?v=A05cBJ_P7Q8






