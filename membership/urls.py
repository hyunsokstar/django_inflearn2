from django.urls import path, re_path , include
from . import views

from django.contrib.auth import views as auth_views
from django.conf import settings

app_name = 'membership'

urlpatterns = [
    path('', include('blog.urls')),
    # re_path(r'^signup/$', views.signup, name='signup'),
    # re_path(r'^profile/$', views.profile, name="profile"),
    re_path(r'^login/$', auth_views.LoginView, name = 'login',  kwargs= {'template_name' : 'accounts/login_form.html'}),
    re_path(r'^logout/$', auth_views.LogoutView, name = 'logout', kwargs = {'next_page' : settings.LOGIN_URL}),
]
