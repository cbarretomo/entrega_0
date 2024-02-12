# entrega_0


Para gerear el docker ejecute el siguiente código:

docker build -t flaskapp

Una vez finalizado el proceso ejecute el siguiente código:
docker run -it --publish 7000:5000 flaskapp

La ruta obtenieda en consola, cambie el puerto 5000 por 7000 y ya podra porbar con postman la aplicación.
