#Python 3.9.5
#Conexion y querys a BBDD
import pymysql as MySQLdb

class db_conn:

    """DB_conn(db_host,db_user,db_pass) 
        Credenciales de la BBDD **
            db_host = Conexión host de la BBDD
            db_user = Usuario de la BBDD
            db_pass = Contraseña del usuario
                                **
    """
    def __init__(self, db_host, db_user, db_pass):
        self.db_host = db_host
        self.db_user = db_user
        self.db_pass = db_pass
        connection = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass)
        self.cursor = connection.cursor()

    def insertarTabla(self, db_name, db_table, address, name):
        """Inserta un registro en la BBDD"""
        insert = "INSERT INTO " + db_name + "." + db_table + " (address, name) VALUES ('" + address + "' , '" + name + "' )"
        print("Insertar - datos " + address + name)
        self.cursor.execute(insert)
        self.cursor.execute("COMMIT")
        result = self.cursor.fetchone()
        print(result)

    def existeRegistro(self, db_name, db_table, address):
        """Comprueba la existencia del registro en la BBDD"""
        existe = "SELECT * FROM " + db_name  + "." + db_table + " WHERE address = '" + address + "'"
        print(existe)
        print("Exists")
        self.cursor.execute(existe)
        if self.cursor.fetchone() is None:
            return False
        else:
            print("El registro ", address, " ya existe.")
            return True
    def ejecutarQuery(self, query):
        self.cursor(query)


