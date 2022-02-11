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


## Volumes

Volume          | Description
----------------|-------------
`/app`          | The location of the DocPad application root.