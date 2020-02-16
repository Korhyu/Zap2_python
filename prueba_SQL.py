import mysql.connector
from mysql.connector import Error
from Zap2_python.sql_functions import funciones


def insertVariblesIntoTable(cad, num):
    #cad = str(input("Ingrese la cadena: "))
    #num = str(input("Ingrese el numero: "))
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='zap2',
                                             user='zap2app',
                                             password='zap2app')
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO prueba (cadena, coma) 
                                VALUES (%s, %s) """

        recordTuple = (cad, num)
        cursor.execute(mySql_insert_query, recordTuple)
        connection.commit()
        print("Datos insertados en la tabla prueba")

    except mysql.connector.Error as error:
        print("Error al insertar en la base de datos {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("Conexion cerada")

funciones.insertar_prueba_db('asdasd', -24)
funciones.insertar_prueba_db('gyhtrh', -30)

