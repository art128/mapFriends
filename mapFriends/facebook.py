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
        + '&scope=email,public_profile,user_friends,user_hometown,user_location,user_about_me' \
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

    redirect_url = urllib.quote_plus(settings.SITE_URL)

    url = 'https://graph.facebook.com/oauth/access_token?' \
          + 'client_id=' + settings.FACEBOOK_APP_ID \
          + '&redirect_uri=' + redirect_url \
          + '&client_secret=' + settings.FACEBOOK_API_SECRET \
          + '&code=' + request.GET['code']

    response = urllib2.urlopen(url).read()


    params = urlparse.parse_qs(response)

    return params

def get_user_data(request, token):
    print "[get_user_data] Obteniendo informacion de uno mismo"
    data = {}

    graph_url = 'https://graph.facebook.com/me?' \
        + 'access_token=' + token
 
    # get the user's data from facebook
    response = urllib2.urlopen(graph_url).read()
    user = json.loads(response)

    data['name'] = user['name']
    data['id'] = user['id']
    data['email'] = user['email']

    graph_url = 'https://graph.facebook.com/me/picture?' \
        + 'type=normal' \
        + '&redirect=false' \
        + '&access_token=' + token

    response = urllib2.urlopen(graph_url).read()

    picture = json.loads(response)

    if not picture['data']['is_silhouette']:
        data['picture'] = picture['data']['url']
    else:
        data['picture'] = ''

    return data

def get_user_friends(request, token):

    data = []
    sites_list = []
    print "[get_user_friends] Obteniendo amigos"
    graph_url = 'https://graph.facebook.com/me/friends?' \
        + 'access_token=' + token

    response = urllib2.urlopen(graph_url).read()
    friends = json.loads(response)

    print "[get_user_friends] Obteniendo lugares e imagenes"
    #Bucle para recorrer todo el array
    for friend in friends['data']:
        dicc = {}
        dicc['name'] = str(friend['name'])
        dicc['id'] = str(friend['id'])
        graph_url = 'https://graph.facebook.com/' \
            + dicc['id'] \
            + '?access_token=' + token

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
            + '&access_token=' + token
        
        response = urllib2.urlopen(graph_url).read()
        picture = json.loads(response)

        if not picture['data']['is_silhouette']:
            dicc['picture'] = str(picture['data']['url'])
        else:
            dicc['picture'] = ''

        data.append(dicc)

    return data, sites_list

def get_coordinates(request, sites, token):
    data = []
    print "[get_coordinates]"
    for site in sites:
        if not site is None:
            position = {}
            graph_url = 'https://graph.facebook.com/' \
                + site \
                + '?access_token=' + token

            response = urllib2.urlopen(graph_url).read()
            coordinates = json.loads(response)
            position['id'] = str(site)
            position['longitude'] = coordinates['location']['longitude']
            position['latitude'] = coordinates['location']['latitude']
            data.append(position)

    return data