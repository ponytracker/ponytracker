from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # django admin
    url(r'^django-admin/', include(admin.site.urls)),
    # login / logout
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    # permissions managment
    url(r'^', include('permissions.urls')),
    # account managment
    url(r'^', include('accounts.urls')),
    # tracker
    url(r'^', include('tracker.urls')),
)
