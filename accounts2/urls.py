from django.urls import path, re_path
from . import views

app_name = 'accounts2'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
]
