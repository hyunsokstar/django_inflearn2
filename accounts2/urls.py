from django.urls import path, re_path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts2'

urlpatterns = [
    # path('', include('blog.urls')),
    path('signup/', views.signup, name='signup'),
    # path('login/', auth_views.LoginView, name = 'login',  kwargs= {'template_name' : 'accounts2/login_form.html'}),

]
