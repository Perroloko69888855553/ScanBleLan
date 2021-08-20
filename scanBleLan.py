
from adafruit_ble import BLERadio
import pymysql as MySQLdb
import json
import os

#Inicializar Variables



def escaneoDispositivos():
    ble = BLERadio()
    print("scanning")
    found = set()
    scan_responses = set()
    print("--------- Inicio de Escaneo ---------")
    #for advertisement in ble.start_scan(timeout=10, buffer_size=1024):
    for advertisement in ble.start_scan(buffer_size=1024):
        addr = advertisement.address
        if advertisement.scan_response and addr not in scan_responses:
            scan_responses.add(addr)
        elif not advertisement.scan_response and addr not in found:
            found.add(addr)
        else:
            continue
        print(addr, advertisement)
        print("\t" + repr(advertisement))
        print()
    print("----",len(scan_responses)," dispositivos encontrados")
    print("--------- Fin de Escaneo ---------")

def escrituraDB():
    c = cargarCreds()
    connection = MySQLdb.connect(host=c["host"], user=c["user"], passwd=c["pass"])
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ble_devices")
    result = cursor.fetchall()
    print(result)
    
def cargarCreds():
    filepath = os.path.dirname(__file__) + "/creds.json"
    print(filepath)
    data = json.load(open(filepath, 'r'))
    return data

escrituraDB()
#escaneoDispositivos()
