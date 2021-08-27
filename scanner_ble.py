#python 3.9.5
from adafruit_ble import BLERadio
import json, os
from config import db_conn as db_obj

def escaneoDispositivos(timeout,buffer_size):  
    ble = BLERadio()
    print("--------- Inicio de Escaneo ---------")
    dispositivos = set()
    responses = set()
    #Iteracion de las llamadas que registra en el escaneo
    for advertisement in ble.start_scan(timeout= timeout, buffer_size=buffer_size):
        if advertisement.address not in responses:
            dispositivos.add(advertisement)
            responses.add(advertisement.address)
            print("Dipositivo encontrado : " + repr(advertisement.address))
    print("Dispositivos encontrados : ", len(dispositivos))
    print("--------- Fin de Escaneo ---------")
    return dispositivos
  
def escaneoBLE():
    #lectura datos json
    json_file = json.load(open(os.path.dirname(__file__) + "/config/conf.json", 'r'))
    #Se cargan los datos de la bbdd y el escaner
    db_data = json_file["db_data"][0]
    ble_scanner = json_file["ble_scanner"][0]
    #Escaneo de dispositivos
    dispositivos = escaneoDispositivos(ble_scanner["scan_timeout"], ble_scanner["buffer_size"])

    if dispositivos is not None:
    #Conexion BBDD
        db = db_obj.db_conn(db_data["host"], db_data["user"], db_data["pass"])
    #Iteraccion para el registro de los dispositivos
        for dispositivo in dispositivos:
            address = repr(dispositivo.address).split("\"")[1]
            name = repr(dispositivo.complete_name) if (dispositivo.complete_name is not None) else "unknow_device"
            #Insertar en la bbdd si no estan guardados            
            if db.existeRegistro(db_data["db_name"],db_data["db_table"],address):
                continue
            else:
               db.insertarTabla(db_data["db_name"],db_data["db_table"],address,name)

    print("Fin del programa")

