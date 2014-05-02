from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('social_auth.urls')),
    url(r'^$', 'mapFriends.views.index', name='index'),
    url(r'^members/', 'mapFriends.views.member', name='member'),
    #url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
