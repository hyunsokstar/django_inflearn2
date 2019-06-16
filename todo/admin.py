from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from . models import Todo, CommentForTodo, Category, Classification, TodoType

@admin.register(TodoType)
class TodoTypeAdmin(admin.ModelAdmin):
    list_display=['type_name']

@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display=['id','name','description','slug']

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
