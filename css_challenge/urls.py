from django.contrib import admin
from django.urls import path, include
from . import views

app_name= 'css_challenge'
urlpatterns = [
    path('', views.css_image_list , name="css_image_list"),
]
