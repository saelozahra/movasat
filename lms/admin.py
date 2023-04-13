from django.contrib import admin
from .models import *
# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "CreatedDate", "view_count", "like_count")
    list_display_links = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ('اطلاعات کلاس', {
            'fields': ('title', 'slug', 'content', 'cover', 'ostad', ),
            'description': 'اطلاعات کلاس',
        }),
        ('جزئیات کلاس', {
            'fields': ('paye', 'day', 'ClassLength', ),
            'description': 'اطلاعات بیشتر و جزئیات کلاس',
            'classes': ('collapse', ),
        }),
    )

admin.site.register(Course, CourseAdmin)
admin.site.register(Section)
admin.site.register(Lesson)
admin.site.register(Teacher)
