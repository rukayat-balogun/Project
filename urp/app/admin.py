# admin.py
from django.contrib import admin
from .models import NewsEvent, Event, Gallery

class NewsEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ['title']
    list_filter = ('date',)
    ordering = ('-date',)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ['title']
    list_filter = ('date',)
    ordering = ('-date',)

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ['title']
    list_filter = ('created_at',)
    ordering = ('-created_at',)

# Registering models with custom admin classes
admin.site.register(NewsEvent, NewsEventAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Gallery, GalleryAdmin)
