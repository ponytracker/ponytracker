from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views


urlpatterns = [
    # django admin
    url(r'^django-admin/', admin.site.urls),
    # login / logout
    url(r'^login$', views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout$', views.LogoutView.as_view(next_page='/'), name='logout'),
    # permissions managment
    url(r'^', include('permissions.urls')),
    # account managment
    url(r'^', include('accounts.urls')),
    # tracker
    url(r'^', include('tracker.urls')),
]
