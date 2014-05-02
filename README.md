                        MAPFRIENDS
=========================================================================

Practica de Programación Integrativa, de la universidad de Informática de A Coruña.

Instalación : (Ubuntu 32bits)

    Si tienes pip instalado puedes saltar el primer paso
        1. sudo apt-get install python-pip
        2. sudo pip install Django==1.6.4

Estructura :

    ├── manage.py
    ├── mapFriends
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── views.py
    │   └── wsgi.py
    ├── README.md
    ├── static
    │   ├── image.jpg
    │   └── style.css
    └── templates
        ├── base.html
        ├── index.html
        └── map.html


    Templates : Se encuentran las vistas de la web, todas extienden de base.html
    mapFriends : Carpeta donde se encuentra la aplicación principal
    static : Archivos estatitos, como los css

Configuración :


    La base de datos es un archivo sqlite que se encuentra en la carpeta anterior 
    al proyecto. Se puede cambiar esto modificando la ruta en el archivo settings.py
    
    Se tienen que definir el ID y el SECRET de la aplicación de facebook.

Dependencias :

    OpenId : python-openid
    OAuth : python-oauth2

Iniciar el servidor :

    Si es la primera vez necesitaras crear las base de datos.
        ./manage.py syncdb
    Para arrancar el servidor
        ./manage.py runserver
