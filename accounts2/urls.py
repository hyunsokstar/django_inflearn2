from django.urls import path, re_path, include
from . import views

app_name = 'accounts2'

urlpatterns = [
    # path('', include('blog.urls')),
    path('signup/', views.signup, name='signup'),
]
