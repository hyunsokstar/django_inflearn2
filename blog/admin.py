from django.contrib import admin
from .models import Post, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name','description','slug']
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','head_image','author','created']
