from django.urls import path, re_path , include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings

app_name = 'skilblog'

urlpatterns = [
    # 1122

    # path('myshortcut/modify_myshortcut_by_summer_note/<int:pk>/', views.modify_myshortcut_by_summer_note.as_view() , name='modify_myshortcut_by_summer_note'),
    path('modify_skilblog_content2_by_summernote/<int:pk>/', views.modify_skilblog_content2_by_summernote.as_view() , name='modify_skilblog_content2_by_summernote'),

    path('edit_skil_blog_for_content1/<int:id>', views.edit_skil_blog_for_content1 , name='edit_skil_blog_for_content1'),
    path('edit_skil_blog_for_content2/<int:id>', views.edit_skil_blog_for_content2 , name='edit_skil_blog_for_content2'),



    # edit_skil_blog_for_content1
    path('new/summernote/<int:skil_blog_title_id>', views.createViewForSkillBlogContentUsingSummerNote.as_view() , name="createViewForSkillBlogContentUsingSummerNote"),

    path('delete_sbc_content/<int:id>', views.delete_sbc_content , name="delete_sbc_content"),
    path('sbc_title_modify/<int:id>', views.sbc_modify , name="sbc_title_modify"),


    path('', views.SkilBlogTitleList.as_view() , name="SkilBlogTitleList"),
    # 스킬 블로그의 상세 보기
    path('<int:id>', views.SkilBlogContentList , name="SkilBlogContentList"),

]
