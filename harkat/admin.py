from django.contrib import admin
from harkat.models import *
# Register your models here.
from unfold.admin import ModelAdmin


@admin.register(Harkat)
class HarkatAdmin(ModelAdmin):
    list_display = ("Title", "Amount", "pool", "MadadKar")
    list_editable = ("Amount", )
    # list_display_links = ("Title", "Slug")
    prepopulated_fields = {"Slug": ("Title",)}
    list_filter = (
        ('MadadKar', 'State')
    )

    def pool(self, obj):
        return obj.total_amount
    pool.allow_tags = True
    pool.short_description = "مبلغ جمع شده"

    fieldsets = (
        ('اطلاعات حرکت', {
            'fields': ('Title', 'Slug', 'Picture', 'Description', ),
            'description': 'اطلاعات کلاس',
        }),
        ('جزئیات حرکت', {
            'fields': ('MadadKar', 'Amount', 'State', ),
            'description': 'اطلاعات بیشتر و جزئیات حرکت',
            # 'classes': ('collapse', ),
        }),
    )


admin.site.register(Transaction)
