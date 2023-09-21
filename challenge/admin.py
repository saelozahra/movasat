from challenge.models import *
from django.contrib import admin
# Register your models here.


class ResponseInline(admin.StackedInline):
    model = Response


class ForumAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "date")
    inlines = [ResponseInline, ]


class DivarAdmin(admin.ModelAdmin):
    # raw_id_fields = ('RelatedProject',)
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'Admin', None) is None:
            obj.Admin = request.user
            obj.save()
        else:
            obj.save()

    list_filter = (
        ('Admin', 'SubmitDate')
    )
    list_display = ("Name", "Status", "Type", "Admin")


admin.site.register(Response)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Divar, DivarAdmin)
