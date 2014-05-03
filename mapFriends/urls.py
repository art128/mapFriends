from django.conf.urls import patterns, url, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','mapFriends.views.index', name='index'),
    url(r'^login/$','mapFriends.views.login', name='login'),
    url(r'^register/$','mapFriends.views.register', name='register'),
  
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
