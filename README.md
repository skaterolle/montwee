# Montwee

Proyecto CRUD para la asignatura de AGI

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 12.2.7.

# Flask Server

En caso de tener que correr el servidor en local, se adjuntan los archivos en una carpeta llamada Flask-Mongo. En esta carpeta Estará el archivo app.py que será el que habrá que ejecutar mediante el comando `python app.py` ó `python3 app.py`. También está el archivo database.yaml del cual leerá la URL para el servidor Mongo, en caso de hacerlo con MongoDB Atlas habrá que realizarlo mediante la url que nos dá el driver de C#/.NET.

En caso de correrlo en un servidor, en el archivo app.py, en el run habrá que hacerlo de la siguiente manera `app.run(host='0.0.0.0')` ya que sin esto el programa no podrá recibir los datos del servidor.

## Dependencias

Las dependencias necesarias para hacer funcionar el servidor de flask serán las siguientes:

- flask
- flask_cors
- pymongo
- pyyaml
- dnspython
- certifi

# MongoDB

Para que la aplicación funcione, el servidor de MongoDB debe de disponer de una Base de Datos llamada Twitter con una colleción llamada tweets donde se guarde toda la información, sino no funcionará. Además habrá que crear un indice de tipo texto. En mi caso, este indice lo creé de la siguiente manera: `db.tweets.createIndex({ text: "text", "user.name": "text", "user.screen_name": "text", "user.description": "text", "place.name": "text", "place.full_name": "text", "place.country": "text", "place.country_name": "text" },{ name: "TextIndex", default_language:"spanish" })`

Para que funcione el programa, la BD debe tener los siguientes parámetros:

- \_id
- created_at
- id
- id_str
- text
- source
- user
- geo
- entities
- retweeted_status
- lang

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Si se va a realizar con electron habrá que hacerlo de la siguiente manera con electron packager`npx electron-packager . Montwee --platform=win32 --arch=x64 `
Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.
