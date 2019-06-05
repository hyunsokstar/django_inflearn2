from django.urls import path, re_path , include
from . import views

from django.contrib.auth import views as auth_views
from django.conf import settings

app_name = 'wm'

urlpatterns = [
    path('myshortcut/', views.MyShortCutListView.as_view() , name="my_shortcut_list"),
    path('new/input', views.MyShortCutCreateView_input.as_view() , name="insert_myshortcut_input"),
    path('new/textarea', views.MyShortCutCreateView_textarea.as_view() , name="insert_myshortcut_textarea"),

    path('myshortcut/delete_shortcut_ajax/<int:id>', views.delete_shortcut_ajax , name="delete_shortcut_ajax"),

    path('myshortcut/category/<str:slug>/', views.MyShortcutListByCategory.as_view()),

    # path('update_comment_ajax/<int:id>', views.update_comment_ajax , name='update_comment_ajax'),
    path('myshortcut/update_shortcut1_ajax/<int:id>', views.update_shortcut1_ajax , name='update_shortcut1_ajax'),
    path('myshortcut/update_shortcut2_ajax/<int:id>', views.update_shortcut2_ajax , name='update_shortcut2_ajax'),


]
