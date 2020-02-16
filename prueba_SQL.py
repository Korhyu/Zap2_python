#SQL
import mysql.connector
from mysql.connector import Error
import time


# Datos de la base de datos
db = mysql.connector.connect(   host="localhost",
                                user="zap2app",
                                passwd="zap2app",
                                db="zap2")


#Funcion ppal, primero verifico que la conexion con la db funcione
try:
    if db.is_connected():
        db_Info = db.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = db.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if (db.is_connected()):
        cursor.close()
        db.close()
        print("MySQL connection is closed")

try:
    cur = db.cursor()
    instruccion = """INSERT INTO prueba(cadena, coma) VALUES ('test', 1)"""
    cur.execute(instruccion)
    cur.close()

except Error as e:
    print("Error enviando el dato ", e)

finally:
    if (db.is_connected()):
        cursor.close()
        db.close()
        print("MySQL connection is closed")