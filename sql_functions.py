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
            connection = mysql.connector.connect(   host = self.host,
                                                    database = self.database,
                                                    user = self.user,
                                                    password = self.password)
            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO medicion (instalacion, tipom, time_id, valor) VALUES (%s, %s, %s, %s) """
            recordTuple = (str(instalacion), str(tipo_med), str(tiempo), str(valor))
            #print(recordTuple)
            cursor.execute(mySql_insert_query, recordTuple)
            connection.commit()
            print("Datos insertados en la tabla medicion")

        except mysql.connector.Error as error:
            print("Error al insertar en la base de datos {}".format(error))

        except:
            print("CAOS MEDICION!!!")

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                #print("Conexion cerrada")

    def insertar_timestamp_db(self, timestamp, uso_horario = 0):
        try:
            connection = mysql.connector.connect(   host = self.host,
                                                    database = self.database,
                                                    user = self.user,
                                                    password = self.password)
            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO tiempo (timestamp, uso_horario) VALUES (%s, %s) """
            recordTuple = (timestamp, uso_horario)
            cursor.execute(mySql_insert_query, recordTuple)
            connection.commit()
            mySql_insert_query = """SELECT MAX(id) FROM tiempo"""
            cursor.execute(mySql_insert_query)
            ultimo_id = cursor.fetchall()
            print("Datos insertados en la tabla time " + timestamp + " " + uso_horario + " " + ultimo_id)

        except mysql.connector.Error as error:
            print("Error al insertar en la base de datos {}".format(error))

        except:
            print("CAOS TEMPORAL!!!")

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                #print("Conexion cerrada")
                return ultimo_id[0][0]
                #return int(ultimo_id[0].split('(')[1].split(',')[0])


    def send_db(self, info):
        datos = electric_data(1, 0)
        datos = info

        datos.time_id = self.insertar_timestamp_db(datos.time_tag)
        self.insertar_medicion_db(10, 1, datos.time_id, datos.ins2eff(datos.v))                 #Tension
        self.insertar_medicion_db(10, 2, datos.time_id, datos.ins2eff(datos.i))                 #Corriente
        self.insertar_medicion_db(10, 3, datos.time_id, datos.cosfi)                            #Cosenofi
        self.insertar_medicion_db(10, 4, datos.time_id, datos.freq)                             #Frecuencia
        self.insertar_medicion_db(10, 5, datos.time_id, datos.ins2eff(datos.pp))                #Potencia Activa
        self.insertar_medicion_db(10, 6, datos.time_id, datos.ins2eff(datos.pq))                #Potencia Reactiva
        self.insertar_medicion_db(10, 7, datos.time_id, datos.ins2eff(datos.ps))                #Potencia Aparente
