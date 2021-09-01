#Python 3.9.5
#App web con el listado de dispositivos.
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_bootstrap import Bootstrap
import json, os
import scanner_ble

#Se instancian las variables de las librerias Flask y Bootstrap.
app = Flask(__name__)
Bootstrap(app)
#Recoge del fichero JSON los datos de la BBDD
json_file = json.load(open(os.path.dirname(__file__) + "/config/conf.json", 'r'))
db_data = json_file["db_data"][0]
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
    date_scan = db.Column(db.DateTime, nullable = False)

#Route ;: Envia los registros de la BBDD
@app.route('/')
def index():
    devices = Device.query.filter().order_by(desc(Device.date_scan)).all()
    return render_template('index.html', devices=devices)

if __name__ == '__main__':
      app.run()