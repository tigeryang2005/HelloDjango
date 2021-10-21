from django.contrib import admin
from . import models
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'author', 'pub_date', 'abstract', 'img_url')
    list_per_page = 10
    ordering = ('id',)
    list_editable = ['name', 'author', 'price']
    search_fields = ('name', 'author', 'publisher')
    list_filter = ('name', 'author')
    # 详细的时间分层筛选
    date_hierarchy = 'pub_date'

admin.site.register(models.Books, BookAdmin)
