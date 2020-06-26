from django.urls import path, re_path, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView


app_name = 'accounts2'

urlpatterns = [
    # path('', include('blog.urls')),
    path('signup/', views.signup, name='signup'),
    path('member_list/', views.member_list, name='member_list'),
    path('my_profile_information_view/', views.my_profile_information_view.as_view(), name = 'my_profile_information_view'),
    path('update_for_profile/<int:id>', views.update_for_profile , name='update_for_profile'),

    # 참고 wm MyShortcutListByUser
    path('user_profile_information_view/<str:user>', views.user_profile_information_view, name="user_profile_information_view"),
    path('delete_login_user/', views.delete_login_user, name="delete_login_user"),


    # path('login/', auth_views.LoginView, name = 'login',  kwargs= {'template_name' : 'accounts2/login_form.html'}),

]
