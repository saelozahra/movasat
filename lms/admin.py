from django.contrib import admin
from .models import *
from inline_ordering.admin import OrderableStackedInline
# Register your models here.


@admin.register(Category)
class CustomCategory(admin.ModelAdmin):
    list_display = ("name", "slug")
    list_display_links = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class LessonInline(OrderableStackedInline):
    model = Lesson
    list_display = ("title", "course",)


class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "CreatedDate", "view_count", "like_count")
    list_display_links = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]
    fieldsets = (
        ('اطلاعات کلاس', {
            'fields': ('title', 'slug', 'content', 'cover', 'category', 'ostad', ),
            'description': 'اطلاعات کلاس',
        }),
        ('جزئیات کلاس', {
            'fields': ('day', 'ClassLength', ),
            'description': 'اطلاعات بیشتر و جزئیات کلاس',
            'classes': ('collapse', ),
        }),
    )


class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "birth", "thumbnail_preview")
    # readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview
    thumbnail_preview.short_description = 'تصویر استاد'
    thumbnail_preview.allow_tags = True


admin.site.register(Course, CourseAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(CourseRegister)
