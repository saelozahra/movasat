from django.db import models

import account.models
from account.models import MadadKar


class Harekat(models.Model):
    class STATE_CHOICES(models.TextChoices):
        ACTIVE = 'active'
        DEACTIVE = 'deactive'
    Title = models.CharField(max_length=110, verbose_name="عنوان")
    Slug = models.SlugField(unique=True, verbose_name="لینک")
    Picture = models.ImageField(upload_to="files/harekat/", verbose_name="تصویر")
    Description = models.TextField(verbose_name="توضیحات")
    MadadKar = models.ForeignKey(MadadKar, on_delete=models.CASCADE, verbose_name="مددکار")
    Amount = models.BigIntegerField(verbose_name="مبلغ")
    TotalAmount = models.BigIntegerField(default=0, editable=False, null=False, blank=False, verbose_name="مبلغ کل")
    State = models.CharField(choices=STATE_CHOICES.choices, default=STATE_CHOICES.ACTIVE, max_length=20, verbose_name="وضعیت")

    class Meta:
        verbose_name = "حرکت"
        verbose_name_plural = "حرکت ها"

    def __str__(self):
        return self.Title
