from django.contrib import admin
from . models import CssImage

# Register your models here.
@admin.register(CssImage)
class CssImageAdmin(admin.ModelAdmin):
    list_display=['id','title','head_image','created', 'author']
