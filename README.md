MapFriends

Practica de la asignatura de Programación Integrativa, de la Universidad De A Coruña

Instalación : (Ubuntu 32bits)

Si tienes pip instalado puedes saltar el primer paso
    1. sudo apt-get install python-pip
    2. sudo pip install Django==1.6.4


Estructura
.
├── manage.py
├── mapFriends
│   ├── admin.py
│   ├── facebook.py
│   ├── forms.py
│   ├── images.py
│   ├── __init__.py
│   ├── models.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── README.md
├── static
│   ├── images
│   ├── script.js
│   └── style.css
└── templates
    ├── base.html
    ├── home.html
    ├── index.html
    ├── login.html
    ├── map.html
    ├── messages.html
    └── register.html

Templates : Se encuentran las vistas de la web, todas extienden de base.html
MapFriends : Carpeta donde se encuentra la aplicación principal
Static : Archivos estatitos, como los css, imagenes ...
Images : Se encuentran las imagenes de perfil


Configuración :

La base de datos es un archivo sqlite que se encuentra en la carpeta anterior 
al proyecto. Se puede cambiar esto modificando la ruta en el archivo settings.py

Se tienen que definir el ID y el SECRET de la aplicación de facebook.


Iniciar el servidor :

Si es la primera vez necesitaras crear las base de datos.
    ./manage.py syncdb
Para arrancar el servidor
    ./manage.py runserver
