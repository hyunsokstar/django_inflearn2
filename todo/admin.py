from . models import Todo, CommentForTodo, Category
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

#Registeryourmodelshere.
# @admin.register(Todo)
# class TodoAdmin(admin.ModelAdmin):
#     list_display=['id','title','author','created',]

class TodoAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'

admin.site.register(Todo, TodoAdmin)


@admin.register(CommentForTodo)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'todo','title', 'text', 'author' ,'created_at' , 'modified_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name','description','slug']
    prepopulated_fields = {'slug': ('name', )}
