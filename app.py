from flask import Flask, render_template, request, url_for, redirect
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

@app.route("/buscarMascota/", methods= ['GET'])
def  mostrarUnaMascota():
    form= BuscarMascotE()
    nombreM= form.nombreM.data
    dnipropietario= form.dnipropietario.data
    insertDate_collection.find({'petName': nombreM} and {'ownerDni': dnipropietario})
    datos= insertDate_collection.find_one()
    return render_template('buscarMascota.html', datos= datos)

# @app.route("/buscarMascota/", methods= ['GET', 'POST'])
# def mostrarMascota():
#     forms= BuscarMascotE()
#     if request.method == 'POST' and forms.validate_on_submit():
#         nombreM= forms.nombreM.data
#         dnipropietario= forms.dnipropietario.data
#         insertDate_collection.find([nombreM])
#         insertDate_collection.find([dnipropietario])







