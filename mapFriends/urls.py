from django.conf.urls import patterns, url, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','mapFriends.views.index', name='index'),
    url(r'^login/$','mapFriends.views.login_view', name='login'),
    url(r'^register/$','mapFriends.views.register', name='register'),
    url(r'^logout/$','mapFriends.views.logout_view', name='logout'),
    url(r'^map/$','mapFriends.views.map', name='map'),
  
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
