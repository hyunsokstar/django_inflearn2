from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from . models import LecRecord, LecInfo

@admin.register(LecInfo)
class LecInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'lec_name','teacher', 'lec_url', 'git_url' ,'deadline', 'rec_reputation','student_count']

@admin.register(LecRecord)
class LecRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'author','current_class', 'perfection', 'note' , 'git_url' , 'created']
