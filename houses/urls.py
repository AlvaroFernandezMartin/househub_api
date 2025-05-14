from django.urls import path

from . import views

app_name = 'houses'

urlpatterns = [
    path('', views.houses_list, name='houses_list'),
]
