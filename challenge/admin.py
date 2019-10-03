from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from . models import StudentRecord, LecInfo, RecommandLecInfo

@admin.register(RecommandLecInfo)
class RecommandLecInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'lecinfo','author']

@admin.register(LecInfo)
class LecInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'lec_name','teacher', 'lec_url', 'git_url' , 'rec_reputation','student_count']

@admin.register(StudentRecord)
class StudentRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'author','current_class', 'created']
