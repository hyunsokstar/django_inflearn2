from django.urls import path, re_path , include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings

app_name = 'skilnote2'


urlpatterns = [

    path('', views.SkilNote2List , name=""),

]
