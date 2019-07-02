from django.urls import path, re_path , include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings

app_name = 'challenge'

urlpatterns = [
    path('<int:classification>', views.LecRecordListView.as_view() , name="lec_record_list"),
    path('lecinfo_list', views.LecInfoListView.as_view() , name="lecinfo_list"),

    path('record/new/<int:classification>',views.CreateRecordView_11.as_view(), name ="네임"),
    path('lec_info/new/',views.CreatelecInfo.as_view(), name ="create_lec_info"),

    path('record/delete/<int:pk>/<int:classification>', views.RecordDeleteView.as_view(), name='student_record_delete'),
    path('record/modify/<int:pk>/<int:classification>', views.RecordUpdateView.as_view(), name='student_record_update'),

    path('lec_info_update/<int:pk>/<int:classification>', views.LecInfoUpdateView.as_view(), name='lec_info_update'),

    path('<int:id>/recommand_lecture/', views.recommand_lecture, name="recommand_lecture"),

]
