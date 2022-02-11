# DocPad Dockerfile

[Docker](http://docker.com) container to use [DocPad](http://docpad.org).


## Uso

### Install

Descargar proyecto del repositorio:

    git clone https://github.com/luismerizalde92/predios.git
    cd predios
    docker-compose up --build

### Comandos imagen django

Recolectar los estaticos y correr las migraciones:

    docker-compose run django_app python backend/manage.py collectstatic --settings=arkandha.settings.production
    docker-compose run django_app python backend/manage.py migrate --settings=arkandha.settings.production


## Services

Service     | Port | Usage
------------|------|------
frontend    | 8081 |  Frontend en Vue, Visite `http://localhost:8081` en su navegador
django_app  | 8000 |  Backend en Django, Visite `http://localhost:8000` en su navegador
db_postgres | 5432 |  Sevicio bases de datos postgres


### Comentarios

Formateo del codigo:

    Para seguir la indicaciones del PEP8 se instalo el paquete flake8

Patrones de diseño:
    se dividiron los requerimientos de acuerdo a la fase de desarrollo
    se dividiron los settings de acuerdo a la fase de desarrollo
    los archivos de la logica de la API se encuentran en una carpeta separada dentro de la misma aplicacion
    se uso un ModelMixin para fecha de creación y de modificación para los dos modelos, este se encuentra en la aplicacion core 

Test Driven Development, para ejecutar pruebas unitarias de la app properties:

    docker-compose run django_app python backend/manage.py test properties --settings=arkandha.settings.production