from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^thanks/(?P<output>\d+)/$', thanks),
]