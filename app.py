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
# insertDate_collection= db.insertDate   ##creando la coleccion
# foudDate_collection= db.foundDate
db= client["dbveterinaria"]


@app.route("/")
def hello():
    return "HELLO WORLD!"

@app.route("/inicio")
def inicio():
    return "Mascota registrada!"


##registrar mascota
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


##buscar mascota
@app.route("/buscarMascota/", methods= ['GET', 'POST'])
def buscarMascota():
    form= BuscarMascotE()
    if request.method == 'POST' and form.validate_on_submit():
        petName= form.petName.data
        ownerDni= form.ownerDni.data
        datos1= db.mascotas.find({'petName': petName, 'ownerDni': ownerDni})
        return render_template('mostrarMascota.html', datos= datos1)
    return render_template('buscarMascota.html', form= form)












# @app.route('/formOrdenar', methods= ['GET','POST'])
# def formOrdenar():
#     if request.method == 'POST':
#         petName= request.form['petName']
#         datePet= request.form['datePet']
#         race= request.form['race']
#         ownerName= request.form['ownerName']
#         ownerDni= request.form['ownerDni']
#         opciones= [nameOrder, dateOrder, raceOrder, ownerDniOrder, ownerNameOrder]
#     return render_template('formOp.html', opciones)

# @app.route('/ordenar', methods=['GET', 'POST'])
# def ordemar():
#     if request.method == 'POST':
#         solicitud= request.form['solicitud']
#         if solicitud == 1 or solicitud == 2 or solicitud == 3 or solicitud == 4 or solicitud == 5 :
#             opcion= insertDate_collection.find('petName': solicitud).sort({''})











