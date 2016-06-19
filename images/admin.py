from django.contrib import admin
from .models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'slug', 'title', 'created']
    list_filter = ['created']


admin.site.register(Image, ImageAdmin)
