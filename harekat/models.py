from django.db import models

import account.models
from account.models import MadadKar


class Harekat(models.Model):
    Title = models.CharField(max_length=110, verbose_name="عنوان")
    Slug = models.SlugField(unique=True, verbose_name="لینک")
    Picture = models.ImageField(verbose_name="تصویر")
    TotalAmount = models.BigIntegerField(verbose_name="مبلغ کل")
    # AmountPerInterest = models.CharField(max_length=110, verbose_name="مبلغ هر سهم")
    Description = models.TextField(verbose_name="توضیحات")
    MadadKar = models.ForeignKey(MadadKar, on_delete=models.CASCADE, verbose_name="مددکار")

    class Meta:
        verbose_name = "حرکت"
        verbose_name_plural = "حرکت ها"

    def __str__(self):
        return self.Title
