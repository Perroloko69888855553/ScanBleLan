
from adafruit_ble import BLERadio
import pymysql as MySQLdb
import json
import os


#Inicializar Variables

def escaneoDispositivos():  
    ble = BLERadio()
    c = cargarJson()
    print("--------- Inicio de Escaneo ---------")
    dispositivos = set()
    responses = set()
    for advertisement in ble.start_scan(timeout= c["scan_timeout"], buffer_size=1024):
        if advertisement.address not in responses:
            dispositivos.add(advertisement)
            responses.add(advertisement.address)
            print("Dipositivo encontrado : " + repr(advertisement.address))
    print("Dispositivos encontrados : ", len(dispositivos))
    print("--------- Fin de Escaneo ---------")
    return dispositivos

def crearDB(): 
    cursor = connectDB()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ble_devices")
    crearTabla()
    cursor.close()
    
def cargarJson():
    filepath = os.path.dirname(__file__) + "/creds.json"
    print(filepath)
    data = json.load(open(filepath, 'r'))
    return data

def crearTabla():
    cursor = connectDB()
    c = cargarJson()
    cursor.execute("USE " + c["db_name"])
    tabla = 'CREATE TABLE IF NOT EXISTS ' + c["db_name"] + "." + c["db_table"]
    cursor.execute( tabla + " (address VARCHAR(255) NOT NULL, name VARCHAR(255) NULL , description VARCHAR(255) NULL , date_scan DATE NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (address))")
    cursor.close()

def connectDB():
    c = cargarJson()
    connection = MySQLdb.connect(host=c["host"], user=c["user"], passwd=c["pass"])
    cursor = connection.cursor()
    print("Conección BBDD")
    return cursor

def insertarTabla(datos):
    cursor = connectDB()
    c = cargarJson()
    insert = "INSERT INTO " + c["db_name"] + "." + c["db_table"] + " (address, name) VALUES (" + datos + " )"
    print("Insertar")
    cursor.execute(insert)
    cursor.execute("COMMIT")
    result = cursor.fetchone()
    print(result)

def existeRegistro(address):
    cursor = connectDB()
    c = cargarJson()
    existe = "SELECT * FROM " + c["db_name"] + "." + c["db_table"] + " WHERE address = '" + address + "'"
    print("Exists")
    cursor.execute(existe)
    if cursor.fetchone() is None:
        return False
    else:
         print("El registro ", address, " ya existe.")
         return True




def escaneoBLE():
    dispositivos = escaneoDispositivos()
    if dispositivos is None:
        print("Fin del programa")
    else:
        for dispositivo in dispositivos:

            datos = "'" + repr(dispositivo.address).split("\"")[1]  + "' , "
            datos += repr(dispositivo.complete_name) if (dispositivo.complete_name is not None) else "'None'"
            
            if existeRegistro(repr(dispositivo.address).split("\"")[1]):
                continue
            else:
                insertarTabla(datos)
            


#crearDB()
#crearTabla()
escaneoBLE()

