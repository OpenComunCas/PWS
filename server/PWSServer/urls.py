from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'([0-9]+)/(luz|temperatura|humedad_relativa|humedad_tierra|distancia|all)$', views.get_all, name='getAll'),
    url(r'([0-9]+)/current$', views.current, name='viewAll'),
    url(r'^$', views.index, name='index'),
    url(r'index.html', views.index, name='index'),
]

