from django.contrib import admin
from . models import MyShortCut, Type, Category

# Register your models here.
@admin.register(MyShortCut)
class MyShortCutAdmin(admin.ModelAdmin):
    list_display=['id','title','content1','content2','created','author','type']

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display=['id','type_name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name','description','slug','author']
    prepopulated_fields = {'slug': ('name', )}
