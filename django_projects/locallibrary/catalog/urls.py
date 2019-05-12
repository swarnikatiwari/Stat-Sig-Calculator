from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    #path('', views.index, name='index'), 
    url(r'^$', views.add, name='add'),
    #url(r'^/', views.thanks , name='thanks'),
    url(r'^thanks/(?P<output>\d+)/$', views.thanks),
]