from django.conf import settings
from django.core.context_processors import csrf
from django.conf import settings
from ctypes import *
import urllib
import urllib2
import urlparse
import json


def get_authorization_url(request):
    
    # URL to where Facebook will redirect to
    redirect_url = urllib.quote_plus(settings.SITE_URL)

    request.session['facebook_state'] = unicode(csrf(request)['csrf_token'])


    # redirect to facebook for approval
    url = 'https://www.facebook.com/dialog/oauth?' \
        + 'client_id=' + settings.FACEBOOK_APP_ID \
        + '&redirect_uri=' + redirect_url \
        + '&scope=email' \
        + '&state=' + request.session['facebook_state']

    return url

def verify(request):
        # Facebook will direct with state and code in the URL
        # ?state=ebK3Np...&code=AQDJEtIZEDU...#_=_
 
        # ensure we have a session state and the state value is the same as what facebook returned
        # also ensure we have a code from facebook (not present if the user denied the application)
        if 'facebook_state' not in request.session \
           or 'state' not in request.GET \
           or 'code' not in request.GET \
           or request.session['facebook_state'] != request.GET['state']:
            return False
        else:
            return True
 
def get_token(request):
 
        # if we don't have a token yet, get one now
        if 'facebook_access_token' not in request.session:
 
            # URL to where we will redirect to
            redirect_url = urllib.quote_plus(settings.SITE_URL)
 
            # set the token URL
            url = 'https://graph.facebook.com/oauth/access_token?' \
                  + 'client_id=' + settings.FACEBOOK_APP_ID \
                  + '&redirect_uri=' + redirect_url \
                  + '&client_secret=' + settings.FACEBOOK_API_SECRET \
                  + '&code=' + request.GET['code']
 
            # grab the token from FB
            response = urllib2.urlopen(url).read()
 
            # parse the response
            # {'access_token': ['AAAGVChRC0ygBAF3...'], 'expires': ['5183529']}
            params = urlparse.parse_qs(response)
 
            # save the token
            request.session['facebook_access_token'] = params['access_token'][0]
            request.session['facebook_access_expires'] = params['expires'][0]

def get_user_data(request):

    data = {}

    graph_url = 'https://graph.facebook.com/me?' \
        + 'access_token=' + request.session['facebook_access_token']
 
    # get the user's data from facebook
    response = urllib2.urlopen(graph_url).read()
    user = json.loads(response)

    data['name'] = user['name']

    graph_url = 'https://graph.facebook.com/me/picture?' \
        + 'type=normal' \
        + '&redirect=false' \
        + '&access_token=' + request.session['facebook_access_token']

    response = urllib2.urlopen(graph_url).read()

    picture = json.loads(response)

    if not picture['data']['is_silhouette']:
        data['picture'] = picture['data']['url']
    else:
        data['picture'] = ''

    return data

def get_user_friends(request):
    data = []
    sites_list = []

    graph_url = 'https://graph.facebook.com/me/friends?' \
        + 'access_token=' + request.session['facebook_access_token']

    response = urllib2.urlopen(graph_url).read()
    friends = json.loads(response)

    #Bucle para recorrer todo el array
    for friend in friends['data']:
        dicc = {}
        dicc['name'] = str(friend['name'])
        dicc['id'] = str(friend['id'])
        graph_url = 'https://graph.facebook.com/' \
            + dicc['id'] \
            + '?access_token=' + request.session['facebook_access_token']

        response = urllib2.urlopen(graph_url).read()
        user = json.loads(response)
        
        if user.has_key('location'):
            dicc['location'] = str(user['location']['id'])
        else:
            dicc['location'] = None

        if user.has_key('hometown'):
            dicc['hometown'] = str(user['hometown']['id'])
        else:
            dicc['hometown'] = None

        if dicc['hometown'] not in sites_list:
            sites_list.append(dicc['hometown'])

        if dicc['location'] not in sites_list:
                sites_list.append(dicc['location'])
        
        graph_url = 'https://graph.facebook.com/' \
            + dicc['id'] \
            + '/picture?' \
            + 'type=square' \
            + '&redirect=false' \
            + '&access_token=' + request.session['facebook_access_token']
        
        response = urllib2.urlopen(graph_url).read()
        picture = json.loads(response)

        if not picture['data']['is_silhouette']:
            dicc['picture'] = str(picture['data']['url'])
        else:
            dicc['picture'] = ''

        data.append(dicc)

    return data, sites_list

def get_coordinates(request, sites):
    data = []

    for site in sites:
        if not site is None:
            position = {}
            graph_url = 'https://graph.facebook.com/' \
                + site \
                + '?access_token=' + request.session['facebook_access_token']

            response = urllib2.urlopen(graph_url).read()
            coordinates = json.loads(response)
            position['id'] = str(site)
            position['longitude'] = coordinates['location']['longitude']
            position['latitude'] = coordinates['location']['latitude']
            data.append(position)

    return data

def download_picture(url, name):
    try:
        furl = urllib2.urlopen(url)
        f = file(name,'wb')
        f.write(furl.read())
        f.close()
    except:
        print 'Unable to download file'

def image_filter(entrada,output):
    libwand=CDLL("libMagickWand.so")
    libwand.MagickWandGenesis()
    mw=libwand.NewMagickWand()
    libwand.MagickReadImage(mw, entrada)
    libwand.MagickTransformImageColorspace(mw,2)
    libwand.MagickWriteImage(mw, output)

def take_image(usuarios):
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


def user_logout(request):
    del request.session['facebook_access_token']
    del request.session['facebook_access_expires']
    if request.session.has_key('facebook_access_token') and request.session.has_key('facebook_access_expires'):
        return False
    else:
        return True