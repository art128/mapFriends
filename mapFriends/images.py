from django.conf import settings
from ctypes import *

def download_picture(url, name):
    print "[download_picture] Descargando imagen"
    try:
        furl = urllib2.urlopen(url)
        f = file(name,'wb')
        f.write(furl.read())
        f.close()
    except:
        print '[donwload_picture] Unable to download file'

def image_filter(entrada,output):
    print "[image_filter] Aplicando filtro"
    libwand=CDLL("libMagickWand.so")
    libwand.MagickWandGenesis()
    mw=libwand.NewMagickWand()
    libwand.MagickReadImage(mw, entrada)
    libwand.MagickTransformImageColorspace(mw,2)
    libwand.MagickWriteImage(mw, output)

def take_image(usuarios):
    print "[take_image] Obteniendo imagenes"
    for usuario in usuarios:
        path_input = settings.BASE_DIR + '/static/images/' + usuario['id'] + '.jpg'
        path_output = settings.BASE_DIR + '/static/images/' + usuario['id'] + '_sepia.jpg'
        download_picture(usuario['picture'], path_input)
        image_filter(path_input, path_output)
        path_output = '/static/images/' + usuario['id'] + '_sepia.jpg'
        usuario['picture'] = path_output
        if usuario['hometown'] is None:
            usuario['hometown'] = "None"
        if usuario['location'] is None:
            usuario['location'] = "None"

    return usuarios