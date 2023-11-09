from django.contrib import admin

from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'header')
    list_filter = ('category', 'author')
    search_fields = ('header',)


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
