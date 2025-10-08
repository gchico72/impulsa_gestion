from django.urls import path
from . import views

app_name = 'cooperadora'

urlpatterns = [
    path('', views.index, name='index'),
]
