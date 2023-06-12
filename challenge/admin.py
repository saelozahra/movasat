from challenge.models import *
from django.contrib import admin
# Register your models here.


class ResponseInline(admin.StackedInline):
    model = Response


class ForumAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "date")
    inlines = [ResponseInline, ]


admin.site.register(Response)
admin.site.register(Forum, ForumAdmin)
