import sqlobject as SO

from ORM_db import Equipo
from ORM_db import Medicion
from ORM_db import Usuario
from ORM_db import Modelo_Equipo
from ORM_db import Time
from ORM_db import Instalacion
from ORM_db import Tipo_Medicion




if __name__ == '__main__':
    # declaro la conexion asi -> "mysql://user:password@host/database"
    connection = SO.connectionForURI("mysql://zap2app:zap2app@localhost:3000/zap2?driver=pymysql")
    SO.sqlhub.processConnection = connection
    # connection.debug = True

    Time()

    Medicion(equipo='10',ubicacion='10',tipom='1',timestamp='1', valor1='120', valor2='130', valor3 = '', valor4='')
    Medicion(equipo='10',ubicacion='10',tipom='1',timestamp='2', valor1='130', valor2='130', valor3 = '', valor4='')
    Medicion(equipo='10',ubicacion='10',tipom='1',timestamp='3', valor1='140', valor2='130', valor3 = '', valor4='')
    Medicion(equipo='10',ubicacion='10',tipom='1',timestamp='4', valor1='150', valor2='130', valor3 = '', valor4='')