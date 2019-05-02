from django.contrib import admin
from .models import Post, Category,Tag, Comment

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display=['id','name','slug']
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name','description','slug']
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','head_image','author','created']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'text', 'author']
