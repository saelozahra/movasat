from django.contrib import admin
from job.models import *
from unfold.admin import ModelAdmin


# Register your models here.

@admin.register(Skills)
class SkillsAdmin(ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Job)
admin.site.register(Category)
