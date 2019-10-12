from django.urls import path, re_path , include
from . import views

from django.contrib.auth import views as auth_views
from django.conf import settings

app_name = 'wm'

urlpatterns = [
    # 1122
    # 체크 박스 체크한 항목들을 스킬 블로그로 이동
    path('myshortcut/move_to_skil_blog/', views.move_to_skil_blog , name='move_to_skil_blog'),

    path('myshortcut/copy_to_me_from_user_id/', views.copy_to_me_from_user_id , name='copy_to_me_from_user_id'),
    path('myshortcut/plus_recommand_for_skillnote_user/', views.plus_recommand_for_skillnote_user , name='plus_recommand_for_skillnote_user'),

    path('myshortcut/edit_complete_skill_note_for_front_end/<int:id>', views.edit_complete_skill_note_for_front_end , name='edit_complete_skill_note_for_front_end'),
    path('myshortcut/edit_complete_skill_note_for_backend/<int:id>', views.edit_complete_skill_note_for_backend , name='edit_complete_skill_note_for_backend'),

    path('myshortcut/edit_temp_skill_note_using_textarea_for_backend/<int:id>', views.edit_temp_skill_note_using_textarea_for_backend , name='edit_temp_skill_note_using_textarea_for_backend'),

    path('myshortcut/edit_temp_skill_note_using_input_for_backend/<int:id>', views.edit_temp_skill_note_using_input_for_backend , name='edit_temp_skill_note_using_input_for_backend'),

    path('myshortcut/update_temp_skil_title_for_backend/<int:id>', views.update_temp_skil_title_for_backend , name="update_temp_skil_title_for_backend"),
    path('myshortcut/delete_temp_skill_note_for_backendarea/<int:id>', views.delete_temp_skill_note_for_backendarea , name="delete_temp_skill_note_for_backendarea"),
    path('myshortcut/insert_temp_skill_note_using_input_for_backend/', views.insert_temp_skill_note_using_input_for_backend , name="insert_temp_skill_note_using_input_for_backend"),
    path('myshortcut/insert_temp_skill_note_using_textarea_for_backend/', views.insert_temp_skill_note_using_textarea_for_backend , name="insert_temp_skill_note_using_textarea_for_backend"),
    path('myshortcut/temp_skill_list_for_backend/', views.temp_skill_list_for_backend , name="temp_skill_list_for_backend"),


    path('myshortcut/insert_temp_skill_note_for_input/', views.insert_temp_skill_note_for_input , name="insert_temp_skill_note_for_input"),
    path('myshortcut/edit_temp_skill_note_for_input/<int:id>', views.edit_temp_skill_note_for_input , name='edit_temp_skill_note_for_input'),

    path('myshortcut/update_temp_skill_note_for_textarea/<int:id>', views.update_temp_skill_note_for_textarea , name='update_temp_skill_note_for_textarea'),


    path('myshortcut/insert_temp_skill_note_for_textarea/', views.insert_temp_skill_note_for_textarea , name="insert_temp_skill_note_for_textarea"),

    path('myshortcut/update_temp_skil_title/<int:id>', views.update_temp_skil_title , name="update_temp_skil_title"),
    path('myshortcut/delete_temp_memo_by_ajax/<int:id>', views.delete_temp_memo_by_ajax , name="delete_temp_memo_by_ajax"),


    path('myshortcut/temp_skill_list/', views.temp_skill_list , name="temp_skill_list"),
    path('myshortcut/search_by_id_and_word/' , views.search_by_id_and_word, name="search_by_id_and_word"),
    path('myshortcut/copyForCategorySubjectToMyCategory/' , views.copyForCategorySubjectToMyCategory, name="copyForCategorySubjectToMyCategory"),

    path('new_comment_for_my_shortcut/<int:shortcut_id>/ajax/' , views.new_comment_for_my_shortcut, name="new_comment_for_my_shortcut"),
    path('update_shortcut_comment_ajax/<int:shortcut_comment_id>' , views.update_comment_for_my_shortcut, name="update_comment_for_my_shortcut"),
    path('delete_shortcut_comment_ajax/<int:shortcut_comment_id>' , views.delete_comment_for_my_shortcut, name="delete_comment_for_my_shortcut"),

    path('myshortcut/update/shortcut_subject/' , views.update_my_shortcut_subject, name="update_my_shortcut_subject"),
    path('myshortcut/', views.MyShortCutListView.as_view() , name="my_shortcut_list"),

    path('myshortcut/create_new1_input/ajax/', views.create_new1_input , name="create_new1_input"),
    path('myshortcut/create_new1_input_between/ajax/<int:current_article_id>', views.create_new1_input_between , name="create_new1_input_between"),

    path('myshortcut/create_new2_textarea/ajax/', views.create_new2_textarea , name="create_new2_textareas"),
    path('myshortcut/create_new2_textarea_between/ajax/<int:current_article_id>', views.create_new2_textarea_between , name="create_new2_textarea_between"),


    path('myshortcut/create_new4_textarea/ajax/', views.create_new4_textarea , name="create_new4_textareas"),

    path('myshortcut/update/category/nick/', views.update_shortcut_nick , name="update_category_nick"),
    path('myshortcut/update/category_nick_by_author/', views.update_shortcut_nick2 , name="update_category_nick2"),

    path('new/input', views.MyShortCutCreateView_input.as_view() , name="insert_myshortcut_input"),
    path('new/input_title/', views.MyShortCutCreateView_image.as_view() , name="MyShortCutCreateView_image"),

    path('new/textarea', views.MyShortCutCreateView_textarea.as_view() , name="insert_myshortcut_textarea"),
    path('new/textarea_summer_note', views.MyShortCutCreateView_textarea_summer_note.as_view() , name="insert_myshortcut_textarea_summer_note"),

    path('new/textarea_summer_note_through/<int:current_article_id>', views.SkilNoteCreateView_summernote_through.as_view() , name="SkilNoteCreateView_summernote_through"),
    path('new/SkilNoteCreateView_image_through/<int:current_article_id>', views.SkilNoteCreateView_image_through.as_view() , name="SkilNoteCreateView_image_through"),

    path('myshortcut/delete_shortcut_ajax/<int:id>', views.delete_shortcut_ajax , name="delete_shortcut_ajax"),
    path('myshortcut/update_shortcut_ajax/<int:id>', views.update_shortcut_ajax , name="update_shortcut_ajax"),


    path('myshortcut/category/<str:slug>/', views.MyShortcutListByCategory.as_view()),
    path('myshortcut/update_shortcut1_ajax/<int:id>', views.update_shortcut1_ajax , name='update_shortcut1_ajax'),

    path('myshortcut/update_shortcut2_ajax/<int:id>', views.update_shortcut2_ajax , name='update_shortcut2_ajax'),

    path('update/shortcut_id_ajax/<int:id>', views.update_shorcut_id_for_user , name="update_shorcut_id_for_user"),

    path('myshortcut/modify_myshortcut_by_summer_note/<int:pk>/', views.modify_myshortcut_by_summer_note.as_view() , name='modify_myshortcut_by_summer_note'),

    # user_id로 shortcut nick list 출력
    path('myshorcut/nicklist/<str:user_name>/', views.CategoryNickListByUserId , name='category_nick_list'),

    # 유저 리스트 출력 for memo
    path('userlist/byajax', views.user_list_for_memo, name = 'user_list_for_memo'),

    path('myshortcut/delete/ajax/', views.delete_myshortcut_by_ajax, name = 'delete_myshortcut_by_ajax'),
    path('myshortcut/update/category/ajax', views.update_category_by_ajax, name = 'update_category_by_ajax'),


]
