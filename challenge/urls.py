from django.urls import path, re_path , include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings

app_name = 'challenge'

urlpatterns = [
    # path('', views.LecRecord.as_view() , name="클래스뷰"),
    path('', views.LecRecordListView.as_view() , name="lec_record_list"),
    path('record/new/',views.CreateRecordView.as_view(), name ="네임"),
    path('record/delete/<int:pk>/', views.RecordDeleteView.as_view(), name='challenge_record_delete'),
    path('record/modify/<int:pk>/', views.RecordUpdateView.as_view(), name=''),    
]
