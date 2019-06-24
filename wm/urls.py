from django.urls import path, re_path , include
from . import views

from django.contrib.auth import views as auth_views
from django.conf import settings

app_name = 'wm'

urlpatterns = [
    path('myshortcut/update/shortcut_subject/' , views.update_my_shortcut_subject, name="update_my_shortcut_subject"),
    path('myshortcut/', views.MyShortCutListView.as_view() , name="my_shortcut_list"),
    path('myshortcut/update/category/nick/', views.update_shortcut_nick , name="update_category_nick"),

    path('new/input', views.MyShortCutCreateView_input.as_view() , name="insert_myshortcut_input"),
    path('new/input_title/', views.MyShortCutCreateView_input_title.as_view() , name="insert_myshortcut_input_title"),

    path('new/textarea', views.MyShortCutCreateView_textarea.as_view() , name="insert_myshortcut_textarea"),
    path('new/textarea_summer_note', views.MyShortCutCreateView_textarea_summer_note.as_view() , name="insert_myshortcut_textarea_summer_note"),

    path('myshortcut/delete_shortcut_ajax/<int:id>', views.delete_shortcut_ajax , name="delete_shortcut_ajax"),
    path('myshortcut/category/<str:slug>/', views.MyShortcutListByCategory.as_view()),
    path('myshortcut/update_shortcut1_ajax/<int:id>', views.update_shortcut1_ajax , name='update_shortcut1_ajax'),

    path('myshortcut/update_shortcut2_ajax/<int:id>', views.update_shortcut2_ajax , name='update_shortcut2_ajax'),
    path('myshortcut/update_shortcut2_ajax/<int:id>', views.update_shortcut2_ajax , name='update_shortcut2_ajax'),

    path('update/shortcut_id_ajax/<int:id>', views.update_shorcut_id_for_user , name="update_shorcut_id_for_user"),

    path('myshortcut/modify_myshortcut_by_summer_note/<int:pk>/', views.modify_myshortcut_by_summer_note.as_view() , name='modify_myshortcut_by_summer_note'),

    # user_id로 shortcut nick list 출력
    path('myshorcut/nicklist/<str:user_name>/', views.CategoryNickListByUserId , name='category_nick_list'),

    # 유저 리스트 출력 for memo
    path('userlist/byajax', views.user_list_for_memo, name = 'user_list_for_memo'),

]
