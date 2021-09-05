#Python 3.9.5
#App web con el listado de dispositivos.
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange

import json, os
import scanner_ble
import pyotp
import webbrowser

#Se instancian las variables de las librerias Flask y Bootstrap.
app = Flask(__name__)
# Clave creada aleatoriamente en base32 para la encriptación de la libreria Flask-WTF
app.config['SECRET_KEY'] = pyotp.random_base32()
Bootstrap(app)
#Recoge del fichero JSON los datos de la BBDD y la configurción de flask
json_file = json.load(open(os.path.dirname(__file__) + "/config/conf.json", 'r'))
db_data = json_file["db_data"][0]
flask_data = json_file["flask_data"][0]
#Realiza el escaneo de dispositivos
scanner_ble.escaneoBLE()
#Configuración y conexion con BBDD
db_uri = 'mysql+pymysql://' + db_data["user"] + ':' + db_data["pass"] + '@' + db_data["host"] + "/" + db_data["db_name"]
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

#Modelo de la tabla de la BBDD
class Device(db.Model):
    __tablename__ = db_data["db_table"]
    address = db.Column(db.String(255), primary_key=True, nullable = False)
    name = db.Column(db.String(255), nullable = True)
    zone = db.Column(db.String(255), nullable = True)
    date_scan = db.Column(db.DateTime, nullable = False)

    def __init__(self, address, name, zone, date_scan):
        self.address = address
        self.name = name
        self.zone = zone
        self.date_scan = date_scan

#Formulario para la modificación de los registros
class editDevice(FlaskForm):
    # identificador del campo
    id_field = HiddenField()
    #Restricciones de los campos Name y Zone
    name = StringField('Nombre del dispositivo', [ InputRequired()])
    zone = StringField('Zona del dispositivo', [ InputRequired()])
    submit = SubmitField('Actualizar')

#Route ;: Muestra el listado de zonas
@app.route('/')
def index():
    try:
        devices = Device.query.filter().order_by(desc(Device.date_scan)).all()
        zones = Device.query.with_entities(Device.zone).distinct().order_by(Device.zone)
        return render_template('index.html', devices=devices, zones=zones)
    except Exception as e:
        # La variable e contiene la descripción del error
        return errorPaginas(e,"index.html")

#Listado de dispositivos filtrado por zona
@app.route('/zona/<zone>')
def zona(zone):
    try:
        devices = Device.query.filter_by(zone=zone).order_by(desc(Device.date_scan)).all()
        return render_template('zona.html', devices=devices, zone=zone)
    except Exception as e:
        # La variable e contiene la descripción del error
        return errorPaginas(e,"zona.html")

# Pagina del formulario de modificación del registro
@app.route('/editar/<address>',  methods=['GET', 'POST'])
def formEditar(address):
    try:
        device = Device.query.filter(Device.address == address).first()
        form1 = editDevice()
        return render_template('editar.html', device=device, zones=device.zone, form1=form1, address=address)
    except Exception as e:
        # La variable e contiene la descripción del error
        return errorPaginas(e,"editar.html")

# Muestra la página resultado al eliminar un registro de la base de datos
@app.route('/resultado/<address>')
def eliminar(address):
    try:
        device = Device.query.filter(Device.address == address).first()
        db.session.delete(device)
        db.session.commit()
        message = f"El registro del dispositivo {device.address} ha sido eliminado."
        return render_template('resultado.html', message=message)
    except Exception as e:
        # La variable e contiene la descripción del error
        return errorPaginas(e,"resultado.html")

# Muestra la página resultado al modificar un registro de la base de datos
@app.route('/resultado/<address>', methods=['POST'])
def editar(address):
    try:
        device = Device.query.filter(Device.address == address).first()
        device.name = request.form['name']
        device.zone = request.form['zone']
        db.session.commit()
        message = f"El registro del dispositivo {device.address} ha sido modificado."
        return render_template('resultado.html', message=message, zone=device.zone)
    except Exception as e:
        # La variable e contiene la descripción del error
        return errorPaginas(e,"resultado.html")

def errorPaginas(exception,pagina):
        error = "<p>Error en la página " + pagina +" :<br>" + str(exception) + "</p>"
        encabezado = '<h1>Fallo en el aplicativo.</h1>'
        return encabezado + error

if __name__ == '__main__':
    app.run(host=flask_data["host"], port=flask_data["port"])
