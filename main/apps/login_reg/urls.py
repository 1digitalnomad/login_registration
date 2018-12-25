from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^success$', views.success, name='success'),
    url(r'^create$', views.create, name='create'),
    url(r'^login$', views.login, name='login')
]
