import sqlobject as SO

class Instalacion(SO.SQLObject):
    equipo = SO.ForeignKey('Equipo', default=None)
    equipo_sup = SO.ForeignKey('Equipo', default=None)
    usuario = SO.ForeignKey('Usuario', default=None)
    equipo = SO.ForeignKey('Equipo', default=None)
    configuracion = SO.ForeignKey('Configuracion', default=None)
    ubicacion = SO.ForeignKey('Ubicacion', default=None)   

class Equipo(SO.SQLObject):
    usuario = SO.ForeignKey('Usuarios', default=None)
    tipo = SO.ForeignKey('Modelo_Equipos', default=None)
    descripcion = SO.StringCol(length=255, varchar=True)
    #configuracion = SO.ForeignKey('Configuraciones', default=None)
    #ubicacion = SO.ForeignKey('Ubicaciones', default=None)

class Medicion(SO.SQLObject):
    instalacion = SO.ForeignKey('Instalacion', default=None)
    tipom = SO.ForeignKey('Tipo_Mediciones', default=None)
    timestamp = SO.ForeignKey('Tiempo', default=None)
    valor1 = SO.StringCol(length=20, varchar=True)
    valor2 = SO.StringCol(length=20, varchar=True)
    valor3 = SO.StringCol(length=20, varchar=True)
    valor4 = SO.StringCol(length=20, varchar=True)

class Alarma(SO.SQLObject):
    medicion = SO.ForeignKey('Medicion', default=None)
    tipo = SO.ForeignKey('Tipo_Alarma', default=None)
    
class Evento(SO.SQLObject):
    instalacion = SO.ForeignKey('Instalacion', default=None)
    timestamp = SO.ForeignKey('Tiempo', default=None)
    tipo = SO.ForeignKey('Tipo', default=None)    

class Usuario(SO.SQLObject):
    nombre = SO.StringCol(length=255, varchar=True)
    apellido = SO.StringCol(length=255, varchar=True)
    usname = SO.StringCol(length=255, varchar=True)
    passw = SO.StringCol(length=255, varchar=True)

class Tipo_Medicion(SO.SQLObject):
    descripcion = SO.StringCol(length=1000, varchar=True)

class Tipo_Alarma(SO.SQLObject):
    descripcion = SO.StringCol(length=1000, varchar=True)

class Tiempo(SO.SQLObject):
    timestamp = SO.StringCol(length=20, varchar=True)
    uso_horario = SO.StringCol(length=20, varchar=True)

class Modelo_Equipo(SO.SQLObject):
    descripcion = SO.StringCol(length=1000, varchar=True)
    voltaje = SO.StringCol(length=20, varchar=True)
    corriente = SO.StringCol(length=20, varchar=True)

class Configuracion(SO.SQLObject):
    config1 = SO.StringCol(length=20, varchar=True)
    config2 = SO.StringCol(length=20, varchar=True)
    config3 = SO.StringCol(length=20, varchar=True)
    config4 = SO.StringCol(length=20, varchar=True)
    config5 = SO.StringCol(length=20, varchar=True)
    config6 = SO.StringCol(length=20, varchar=True)
    config7 = SO.StringCol(length=20, varchar=True)
    config8 = SO.StringCol(length=20, varchar=True)
    config9 = SO.StringCol(length=20, varchar=True)
    config10 = SO.StringCol(length=20, varchar=True)

class Ubicacion(SO.SQLObject):
    link = SO.StringCol(length=2000, varchar=True)

if __name__ == '__main__':
    connection = SO.connectionForURI("mysql://zap2app:zap2app@localhost:3000/zap2?driver=pymysql")
    SO.sqlhub.processConnection = connection

    #Bajo las tablas si existen
    Instalacion.dropTable(ifExists=True)
    Equipo.dropTable(ifExists=True)
    Medicion.dropTable(ifExists=True)
    Alarma.dropTable(ifExists=True)
    Evento.dropTable(ifExists=True)
    Usuario.dropTable(ifExists=True)
    Tipo_Medicion.dropTable(ifExists=True)
    Tipo_Alarma.dropTable(ifExists=True)
    Tiempo.dropTable(ifExists=True)
    Modelo_Equipo.dropTable(ifExists=True)
    Configuracion.dropTable(ifExists=True)

    #Creo las tablas
    Instalacion.createTable()
    Equipo.createTable()
    Medicion.createTable()
    Alarma.createTable()
    Evento.createTable()
    Usuario.createTable()
    Tipo_Medicion.createTable()
    Tipo_Alarma.createTable()
    Tiempo.createTable()
    Modelo_Equipo.createTable()
    Configuracion.createTable()

    #Query personalizada
    #query = "SELECT artist.name, album.title FROM artist, album 
    # WHERE artist.id=album.artist_id AND artist.name LIKE '%s%%'" % init
    #connection.queryAll(query):

    #Datos hardcodeados
    Usuario(nombre='Prueba',apellido='Prueba',usname='admin',passw='admin')

    Modelo_Equipo(descripcion='Raspberry')
    Modelo_Equipo(descripcion='EG-01 - Medidor de tension y corriente monofasico', voltage='1', corriente='1')
    Modelo_Equipo(descripcion='EG-02 - Medidor de tension y corriente trifasico', voltage='3', corriente='3')
    Modelo_Equipo(descripcion='EG-03 - Medidor de tension y corriente tetrapolar', voltage='3', corriente='4')

    Equipo(tipo='1', descripcion='Raspberry de prueba')
    Equipo(tipo='2', descripcion='Medidor de prueba 1')
    Equipo(tipo='3', descripcion='Medidor de prueba 2')

    Configuracion(uso_horario='-3', config1='5')

    Instalacion(equipo='1',usuario='1')
    Instalacion(equipo='2',usuario='1')

    Tiempo(timestamp='2019-11-20 00:00:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:01:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:02:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:03:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:04:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:05:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:06:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:07:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:08:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:09:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:10:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:11:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:12:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:13:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:14:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:15:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:16:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:17:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:18:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:19:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:20:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:21:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:22:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:23:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:24:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:25:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:26:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:27:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:28:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:29:00', uso_horario='-3')
    Tiempo(timestamp='2019-11-20 00:30:00', uso_horario='-3')
