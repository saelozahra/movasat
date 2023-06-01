from django.contrib import admin
from django.utils.safestring import mark_safe
from harkat.models import *
from harkat.views import percentage
# Register your models here.
from unfold.admin import ModelAdmin


@admin.register(Harkat)
class HarkatAdmin(ModelAdmin):
    list_display = ("Title", "Amount", "pool", "percent", "MadadKar")
    list_editable = ("Amount", )
    # list_display_links = ("Title", "Slug")
    prepopulated_fields = {"Slug": ("Title",)}
    list_filter = (
        ('MadadKar', 'State')
    )

    def pool(self, obj):
        return f"{obj.total_amount:,} تومان"
    pool.allow_tags = True
    pool.short_description = "مبلغ جمع شده"

    @mark_safe
    def percent(self, obj):
        percent = percentage(obj.Amount, obj.total_amount)
        amount = f" {percent}% <div style='width:100%; float:right; height: 10px;background-color: #c084fc;" \
                 f"border-radius: 7px;border: 1px solid #581c87;'><span style='background-color:#7e22ce;height: 100%;" \
                 f" width:{percent}%; float:left;'></span></div>"
        return amount
    percent.allow_tags = True
    percent.short_description = "درصد تکمیل"

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
