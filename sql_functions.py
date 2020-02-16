import mysql.connector
from mysql.connector import Error

datos = ''' host='localhost',
            database='zap2',
            user='zap2app',
            password='zap2app' '''


class funcionesSQL:
    def __init__ (self):
        pass

    def insertar_prueba_db(self, cadena, valor):
        try:
            connection = mysql.connector.connect(   host='localhost',
                                                    database='zap2',
                                                    user='zap2app',
                                                    password='zap2app' )
            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO prueba (cadena, coma) VALUES (%s, %s) """
            recordTuple = (cadena, valor)
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

    def insertar_medicion_db(self, instalacion, tipo_med, tiempo, valor):
        try:
            connection = mysql.connector.connect( self.datos )
            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO medicion (instalacion, tipom, timestamp, valor) VALUES (%s, %s, %s, %s) """
            recordTuple = (instalacion, tipo_med, tiempo, valor)
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


    