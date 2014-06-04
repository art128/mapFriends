from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mapFriends.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'mapFriends.views.home', name='home'),
    url(r'^login/', 'mapFriends.views.login_view', name='login'),
    url(r'^auth/', 'mapFriends.views.auth', name='auth'),
    url(r'^map/', 'mapFriends.views.map', name='map'),
    url(r'^logout/', 'mapFriends.views.logout_view', name='logout'),
    url(r'^register/', 'mapFriends.views.register', name='register'),
    url(r'^admin/', include(admin.site.urls)),
)
