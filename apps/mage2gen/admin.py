from django.contrib import admin

from .models import Module

class ModuleAdmin(admin.ModelAdmin):
	search_fields = ['package_name', 'name']
	list_display = ('created_at', 'package_name', 'name', 'user', 'download_count')
	ordering = ('-created_at',)

admin.site.register(Module, ModuleAdmin)