import mysql.connector
from mysql.connector import Error
from electric_data import electric_data


class funcionesSQL:
    def __init__ (self):
        self.host='localhost'
        self.database='zap2'
        self.user='zap2app'
        self.password='zap2app'


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

    def insertar_medicion_db(self, instalacion, tipo_med, tiempo, valor):
        try:
            print("0")
            connection = mysql.connector.connect(   host = self.host,
                                                    database = self.database,
                                                    user = self.user,
                                                    password = self.password)
            print("1")
            cursor = connection.cursor()
            print("2")
            mySql_insert_query = """INSERT INTO medicion (instalacion, tipom, time_id, valor) VALUES (%s, %s, %s, %s) """
            print("3")
            recordTuple = (str(instalacion), str(tipo_med), str(tiempo), str(valor))
            print(recordTuple)
            cursor.execute(mySql_insert_query, recordTuple)
            print("5")
            connection.commit()
            print("Datos insertados en la tabla medicion")

        except mysql.connector.Error as error:
            print("Error al insertar en la base de datos {}".format(error))

        except:
            print("CAOS!!!")

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Conexion cerrada")

    def insertar_timestamp_db(self, timestamp, uso_horario = None):
        try:
            connection = mysql.connector.connect( self.conn )
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
                print("Conexion cerrada")
                return ultimo_id


    def send_db(self, info):
        datos = electric_data(1, 0)
        datos = info

        datos.time_id = self.insertar_timestamp_db(datos.time_tag)
        self.insertar_medicion_db(10, 1, datos.time_id, datos.ins2eff(datos.v))              #Tension
        #self.insertar_medicion_db(10, 2, datos.time_id, datos.ins2eff(datos.i))              #Corriente
