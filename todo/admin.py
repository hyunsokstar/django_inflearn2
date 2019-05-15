from . models import Todo, CommentForTodo, Category
from django.contrib import admin

#Registeryourmodelshere.
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display=['id','title','author','created',]

@admin.register(CommentForTodo)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'todo','title', 'text', 'author' ,'created_at' , 'modified_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name','description','slug']
    prepopulated_fields = {'slug': ('name', )}
