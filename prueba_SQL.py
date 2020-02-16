import mysql.connector
from mysql.connector import Error

def insertVariblesIntoTable():
    cad = str(input("Ingrese la cadena: "))
    num = str(input("Ingrese el numero: "))
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
        print("Record inserted successfully into prueba table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

insertVariblesIntoTable()
insertVariblesIntoTable()
insertVariblesIntoTable()
