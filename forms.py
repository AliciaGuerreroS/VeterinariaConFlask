from flask_wtf import FlaskForm
from wtforms import  StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, Length


class RegistrandoM(FlaskForm):
    petName= StringField('Nombre_mascota', validators=[DataRequired(), Length(max=50)])
    datePet= DateField('Fecha_nacimiento_mascota')
    race= StringField('Raza', validators=[DataRequired(), Length(max=50)])
    ownerName= StringField('Nombre_propietario', validators=[DataRequired(), Length(max=50)])
    ownerDni= StringField('DNI_propietario', validators=[DataRequired(), Length(max=50)])
    submit= SubmitField('Enviar')

class BuscarMascotE(FlaskForm):
    nombreM= StringField('Ingrese el nombre de la mascota', validators=[DataRequired(), Length(max=50)])
    dnipropietario= StringField('Ingrese el DNI del propietario', validators=[DataRequired(), Length(max=50)])
    buscar= SubmitField('Buscar')
