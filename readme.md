1)LOS EJERCICIOS DE ESTE PROYECTO FUERON DESAROLLADOS EN Python 3.8.5 CON EL MICROFRAMEWORK FLASK, USANDO DOCKER Y BASE DE DATOS MYSQL.

PUEDE EJECUTAR:
(ruta)\venv\scripts\activate.bat

2)EN EL ARCHIVO REQUIREMENTS SE ENCUENTRA TODAS LAS DEPENDENCIAS USADAS. PARA SER INSTALADA SOLO EJECUTE EL COMANDO
pip install -r requirement.txt

3)INICIAR DOCKER EN SU EQUIPO Y ARRANCAR EL CONTENEDOR DE LA BASE DE DATOS
COMANDOS:

docker run -p 3306:3306 --name mysql -v C:\Users\Pc\Desktop\dockerTest\dockerbd\mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=secret -d mysql:latest --character-set-server=utf8 --collation-server=utf8_unicode_ci
docker exec -it mysql mysql -uroot -p

DATABASE_URI ='mysql+pymysql://root:secret@127.0.0.1:3306/enviame' -> en mi caso use la herramienta visual MYSQL-WORKBENCH para interactuar con la base de datos.

existen dos tablas:
-enviame = para el ejercicio 2
-ejercicio7 = para el mismo ejercicio7


4)INICIAR EL PROYECTO CON:  python src/app.py

5)EN EL LINK http://10.42.0.203:4000/     SE PUEDE OBSERVAR LAS RUTAS DE TODOS LOS EJERCICIOS, CON ALGUNAS OBSERVACIONES Y NOTAS.    
