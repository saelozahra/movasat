from madadyar.models import Aghlam, Bohran
from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin


@admin.register(Aghlam)
class AghlamAdminClass(ModelAdmin):
    pass


@admin.register(Bohran)
class BohranAdminClass(ModelAdmin):
    pass
