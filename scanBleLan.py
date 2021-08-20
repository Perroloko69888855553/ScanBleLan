
from adafruit_ble import BLERadio
import pymysql as MySQLdb

#variables Iniciales
db_host = "localhost"
db_user = "root"
db_pass = ""

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
    connection = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass)
    cursor = connection.cursor()
    
        cursor.execute("CREATE DATABASE IF NOT EXISTS ble_devices")       
    

            
escrituraDB()
#escaneoDispositivos()
