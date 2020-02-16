import mysql.connector
from mysql.connector import Error

connection = mysql.connector(host='localhost',
                                             database='zap2',
                                             user='zap2app',
                                             password='zap2app')



def insertVariblesIntoTable(cad, num):
    #cad = str(input("Ingrese la cadena: "))
    #num = str(input("Ingrese el numero: "))
    try:
        connection.connect()
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

insertVariblesIntoTable('asdasd', -24)
insertVariblesIntoTable('gyhtrh', -30)

