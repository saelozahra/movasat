from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserAdmin
from django.contrib.auth.models import User
from .models import *
from unfold.admin import ModelAdmin

UserAdmin.fieldsets += (
    ("حساب کاربری", {"fields": ("is_job_finder", "skills", "City", )}),
)
# UserAdmin.fieldsets[2][1]["fields"] += "skills"
permission_list = list(UserAdmin.fieldsets[1][1]["fields"])
permission_list.append("tel")
permission_list.append("melli")
permission_list.append("birth")
UserAdmin.fieldsets[1][1]["fields"] = permission_list


admin.site.register(UserDetail, UserAdmin)


@admin.register(MadadKar)
class MadadkarAdmin(ModelAdmin):
    list_display = ("Name", "user", "GroupType", "City",)
    list_filter = (
        ('GroupType', 'City')
    )

    fieldsets = (
        ('اطلاعات مددکار', {
            'fields': ('GroupType', 'user', 'Name', 'RegisterCode', 'Bio', 'City', 'Location', 'Address', ),
            'description': 'مشخصات مددکار را وارد کنید',
        }),
        ('تصاویر', {
            'fields': ('Avatar', 'Cover',),
            'description': 'تصاویر گروه جهادی',
        }),
        ('شبکه های اجتماعی', {
            'fields': ('Url', 'Tel', 'Eita', 'Rubika', 'Bale', ),
            'description': 'لینک تشکیلات شما در شبکه های اجتماعی',
            # 'classes': ('collapse', ),
        }),
    )
