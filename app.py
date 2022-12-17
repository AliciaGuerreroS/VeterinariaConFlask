from flask import Flask, render_template, request, url_for, redirect, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from forms import RegistrandoM, BuscarMascotE, MascotaPropietario, ActualizarDato
from flask_wtf import CSRFProtect
from config import Config
import datetime



app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect()
client= MongoClient('localhost', 27017)
db = client.veterinaria
# insertDate_collection= db.insertDate   ##creando la coleccion
# foudDate_collection= db.foundDate
db= client["dbveterinaria"]


@app.route("/")
def hello():
    return "HELLO WORLD!"


##•	Listar todas las mascotas registradas en la veterinaria ordenadas por: fecha de nacimiento, nombre, raza o nombre del propietario.
@app.route('/opciones')
def opciones():
    mascotas=db.mascotas.find().sort('petName',1)
    return render_template("opciones.html", mascotas= mascotas)

@app.route("/porNombre", methods= ['GET', 'POST'])
def porNombre():
    mascotas=db.mascotas.find().sort('petName',1)
    return render_template("pruebaMostrar.html", mascotas=mascotas)

@app.route("/porRaza", methods= ['GET', 'POST'])
def porRaza():
    mascotas=db.mascotas.find().sort('race',1)
    return render_template("pruebaMostrar.html", mascotas=mascotas)

@app.route("/porNPropietario", methods= ['GET', 'POST'])
def porNPropietario():
    mascotas=db.mascotas.find().sort('ownerName',1)
    return render_template("pruebaMostrar.html", mascotas=mascotas)

@app.route("/porDniPropietario", methods= ['GET', 'POST'])
def porDniPropietario():
    mascotas=db.mascotas.find().sort('ownerDni',1)
    return render_template("pruebaMostrar.html", mascotas=mascotas)

@app.route("/porFecha", methods= ['GET', 'POST'])
def porFecha():
    mascotas=db.mascotas.find().sort('datePet',1)
    return render_template("pruebaMostrar.html", mascotas=mascotas)

##•	Registrar los datos de una mascota.

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
        db.mascotas.insert_one({'petName': petName, 'datePet': final_date, 'race': race, 'ownerName': ownerName, 'ownerDni': ownerDni})

        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('inicio'))
    return render_template("registrar.html", form= form)


##•	Mostrar los datos de una determinada mascota.
@app.route("/buscarMascota/", methods= ['GET', 'POST'])
def buscarMascota():
    form= BuscarMascotE()
    if request.method == 'POST' and form.validate_on_submit():
        petName= form.petName.data
        ownerDni= form.ownerDni.data
        datos1= db.mascotas.find({'petName': petName, 'ownerDni': ownerDni})
        return render_template('mostrarMascota.html', datos= datos1)
    return render_template('buscarMascota.html', form= form)


##•	Listar todas las mascotas de un determinado propietario.
@app.route("/mascotaPropietario/", methods= ['GET', 'POST'])
def mascotaPropietario():
    form= MascotaPropietario()
    if request.method == 'POST' and form.validate_on_submit():
        ownerDni= form.ownerDni.data
        datos2= db.mascotas.find({'ownerDni': ownerDni})
        return render_template('mascotaPropietario.html', datosMascota= datos2)
    return render_template('formBPropietario.html', form= form)

##•	Actualizar los datos de una mascota.

@app.route("/actualizarMascota", methods= ['GET', 'POST'])
def actualizarMascota():
    form= ActualizarDato()
    if request.method == 'POST' and form.validate_on_submit():
        petName= form.petName.data
        datePet= form.datePet.data
        time = datetime.datetime.min.time()
        final_date = datetime.datetime.combine(datePet, time)
        race= form.race.data
        ownerName= form.ownerName.data
        ownerDni= form.ownerDni.data
        db.mascotas.find({'petName': petName, 'ownerDni': ownerDni})
        actualizados= db.mascotas.update_one({'ownerDni': ownerDni}, {'$set': {'petName': petName, 'datePet': final_date, 'race': race, 'ownerName': ownerName, 'ownerDni': ownerDni}})
        return render_template('datosActualizados.html', actualizados= actualizados)
    return render_template('buscarDatosActualizar.html', form= form)

















