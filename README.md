# Prueba_t360c

## Descripción

Esta es una pequeña demo para demostrar la integración de auth0 con una aplicación web escrita en Flask.

Simula una versión extremadamente simple de AirBnB. Se requiere un usuario para crear y reservar estancias ("Stays"), pero cualquier persona puede entrar a ver qué estancias hay.

Ya que ingresó, el usuario puede registrar una estancia usando el formato. Éste contiene dos campos: Un título y la localización de la estancia. Por lo tanto, podría crear una estancia llamada "Bello Departamento" en "Nueva York" y así se mostrará en la lista de estancias.

También puede reservar estancias disponibles y borrar sus propias estancias.

## Instalación e inicio

### Instalar requerimientos de python con el siguiente comando

> pip install -r requirements.txt

### Guardar el archivo .env

Si tiene autorización para usar esta aplicación, se le debe haber hecho llegar un archivo ".env" por otro medio. Simplemente guárdelo en el directorio root del proyecto (el mismo que contiene el archivo "server.py")

### Iniciar el servidor

> flask --app server run

Correrá en http://localhost:3000