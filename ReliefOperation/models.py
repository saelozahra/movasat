from django.db import models
from account.models import MadadKar, UserDetail

# Create your models here.


class STATE_CHOICES(models.TextChoices):
    ACTIVATE = 'activate'
    DEACTIVATE = 'deactivate'
class JahadActivity(models.Model):
    Admin = models.ForeignKey(UserDetail, on_delete=models.CASCADE, verbose_name="مدیر")
    Title = models.CharField(max_length=110, verbose_name="عنوان")
    Slug = models.SlugField(unique=True, verbose_name="لینک")
    Picture = models.ImageField(upload_to="files/jahad_activity/", verbose_name="تصویر")
    Description = models.TextField(verbose_name="توضیحات")
    MadadKar = models.ForeignKey(MadadKar, on_delete=models.CASCADE, verbose_name="مددکار")
    Amount = models.BigIntegerField(verbose_name="مبلغ")
    TotalAmount = models.BigIntegerField(default=0, editable=False, null=False, blank=False, verbose_name="مبلغ کل")
    State = models.CharField(choices=STATE_CHOICES.choices, default=STATE_CHOICES.ACTIVATE, max_length=20, verbose_name="وضعیت")

    class Meta:
        verbose_name = "فعالیت های جهادی"
        verbose_name_plural = "فعالیت جهادی"

    def __str__(self):
        return self.Title


class AidOperation(models.Model):
    Admin = models.ForeignKey(UserDetail, on_delete=models.CASCADE, verbose_name="مدیر")
    Title = models.CharField(max_length=110, verbose_name="عنوان")
    Slug = models.SlugField(unique=True, verbose_name="لینک")
    Picture = models.ImageField(upload_to="files/jahad_activity/", verbose_name="تصویر")
    Description = models.TextField(verbose_name="توضیحات")
    # MadadKar = models.ForeignKey(MadadKar, on_delete=models.CASCADE, verbose_name="مددکار")
    Amount = models.BigIntegerField(verbose_name="مبلغ")
    TotalAmount = models.BigIntegerField(default=0, editable=False, null=False, blank=False, verbose_name="مبلغ کل")
    State = models.CharField(choices=STATE_CHOICES.choices, default=STATE_CHOICES.ACTIVATE, max_length=20, verbose_name="وضعیت")

    class Meta:
        verbose_name = "عملیات های کمک رسانی"
        verbose_name_plural = "عملیات کمک رسانی"

    def __str__(self):
        return self.Title