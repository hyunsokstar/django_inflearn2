from django.contrib import admin
from . models import Todo , TodoComplete

#Registeryourmodelshere.
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display=['id','title','author','created',]

@admin.register(TodoComplete)
class TodoCompleteAdmin(admin.ModelAdmin):
    list_display=['id','title','author','created','elapsed_time']
