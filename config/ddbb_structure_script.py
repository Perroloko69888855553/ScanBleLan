#Python 3.9.5
# Script para la creación de la estructura de la BBDD
import json, os
import db_conn

def crearDB(): 
    json_file = json.load(open(os.path.dirname(__file__) + "/config/conf.json", 'r'))
    db_data = json_file["db_data"][0]
    db = db_conn.db_conn(db_data["host"], db_data["user"], db_data["db_pass"])
    db.ejecutarQuery("CREATE DATABASE IF NOT EXISTS " + db_data["db_name"])
    crearTabla(db,db_data["db_name"],db_data["db_table"])

def crearTabla(db,db_name,db_table):
    tabla_query = 'CREATE TABLE IF NOT EXISTS ' + db_name + "." + db_table
    db.ejecutarQuery( tabla_query + " (address VARCHAR(255) NOT NULL, name VARCHAR(255) NULL , zone VARCHAR(255) NULL , date_scan DATE NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (address))")
    
crearDB()