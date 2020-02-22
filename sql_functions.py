import mysql.connector
from mysql.connector import Error
import datetime

datos = ''' host='localhost',
            database='zap2',
            user='zap2app',
            password='zap2app' '''


class funcionesSQL:
    def __init__ (self):

        datos = ''' host='localhost',
                    database='zap2',
                    user='zap2app',
                    password='zap2app' '''

        pass

    def test_db_conn(self):
        try:
            if self.is_connected():
                db_Info = self.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)

        except Error as e:
            print("Error while connecting to MySQL", e)

        finally:
            if (self.is_connected()):
                cursor.close()
                self.close()
                print("MySQL connection is closed")

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
            print("Datos insertados en la tabla medicion")

        except mysql.connector.Error as error:
            print("Error al insertar en la base de datos {}".format(error))

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Conexion cerada")

    def insertar_timestamp_db(self, timestamp, uso_horario = None):
        try:
            connection = mysql.connector.connect( self.datos )
            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO tiempo (timestamp, uso_horario) VALUES (%s, %s) """
            recordTuple = (timestamp, uso_horario)
            cursor.execute(mySql_insert_query, recordTuple)
            connection.commit()
            mySql_insert_query = """SELECT MAX(id) FROM tiempo"""
            cursor.execute(mySql_insert_query)
            ultimo_id = cursor.fetchall()
            print("Datos insertados en la tabla time")

        except mysql.connector.Error as error:
            print("Error al insertar en la base de datos {}".format(error))

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Conexion cerada")
                return ultimo_id

    def get_hora(self):
        fecha = str(datetime.datetime.now())
        fecha = fecha[:19]
        return fecha