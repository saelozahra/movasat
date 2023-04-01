from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserDetail, MadadJoo
from unfold.admin import ModelAdmin

# Define an inline admin descriptor for Employee model


@admin.register(MadadJoo)
class CustomAdminClass(ModelAdmin):
    pass


# which acts a bit like a singleton
class UserDetailInline(admin.StackedInline):

    model = UserDetail
    can_delete = False
    verbose_name_plural = 'کاربر'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserDetailInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
