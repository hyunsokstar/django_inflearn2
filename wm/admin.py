from django.contrib import admin
from . models import MyShortCut, Type, Category,CategoryNick,CommentForShortCut, TempMyShortCut, TempMyShortCutForBackEnd

# Register your models here.

@admin.register(TempMyShortCutForBackEnd)
class TempMyShortCutForBackEndAdmin(admin.ModelAdmin):
    list_display=['id','title','content1','content2','created','author','type']

@admin.register(TempMyShortCut)
class TempMyShortCutAdmin(admin.ModelAdmin):
    list_display=['id','title','content1','content2','created','author','type']

@admin.register(MyShortCut)
class MyShortCutAdmin(admin.ModelAdmin):
    list_display=['id','title','content1','content2','created','author','type']

@admin.register(CategoryNick)
class CategoryNickAdmin(admin.ModelAdmin):
    list_display=['id','ca_subtitle']

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display=['id','type_name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name','description','slug','author']
    prepopulated_fields = {'slug': ('name', )}

@admin.register(CommentForShortCut)
class CommentForShortCutAdmin(admin.ModelAdmin):
    list_display = ['title','content','author','created_at']
