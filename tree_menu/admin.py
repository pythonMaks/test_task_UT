from django.contrib import admin
from .models import MenuItem

from django.contrib import admin
from .models import MenuItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'menu_name', 'parent']
    list_filter = ['name']
    search_fields = ['name', 'menu_name']
