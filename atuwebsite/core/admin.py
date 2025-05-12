from django.contrib import admin
from .models import Service, Course

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'service', 'semester', 'is_paid', 'price')
    list_filter = ('service', 'semester', 'is_paid')
    search_fields = ('course_name', 'description')
