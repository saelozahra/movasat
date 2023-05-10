from django.db import models
from account.models import MadadKar, UserDetail
from django_jalali.db import models as jmodels
# Create your models here.


class StateChoices(models.TextChoices):
    Activate = 'در حال جمع آوری کمک'
    Deactivate = 'به نتیجه رسیده'
    Stopped = 'متوقف شده'


class Harkat(models.Model):
    Title = models.CharField(max_length=110, verbose_name="عنوان حرکت")
    Slug = models.SlugField(unique=True, verbose_name="لینک")
    Picture = models.ImageField(upload_to="files/jahad_activity/", verbose_name="تصویر")
    Description = models.TextField(verbose_name="توضیحات")
    MadadKar = models.ForeignKey(MadadKar, on_delete=models.CASCADE, verbose_name="مددکار")
    Amount = models.BigIntegerField(verbose_name="کل مبلغ مورد نیاز")
    State = models.CharField(choices=StateChoices.choices, default=StateChoices.Activate, max_length=20, verbose_name="وضعیت")

    class Meta:
        verbose_name = "عملیات های کمک رسانی"
        verbose_name_plural = "عملیات کمک رسانی"

    def __str__(self):
        return self.Title

    @property
    def total_amount(self):
        return sum([item.total_amount for item in Transaction.objects.filter(harkat=self).all()])


class Transaction(models.Model):
    class StatusChoices(models.TextChoices):
        X = 'نا موفق'
        N = 'پرداخت نشده'
        S = 'پرداخت شده'

    harkat = models.ForeignKey(Harkat, on_delete=models.CASCADE, verbose_name="حرکت")

    # Purchaser = models.ForeignKey(UserDetail, on_delete=models.CASCADE, verbose_name="خریدار")

    Purchaser = models.CharField(max_length=202, blank=True, verbose_name="نام واریز کننده")

    PurchaserTel = models.CharField(max_length=12, blank=True, verbose_name="شماره تماس واریز کننده")

    PurchaserIP = models.CharField(max_length=16, editable=False, verbose_name="آیپی خریدار")

    PurchaseID = models.CharField(max_length=202, verbose_name="شناسه واریز")

    PurchaseTime = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ واریز")

    Amount = models.CharField(max_length=200, verbose_name="مبلغ")

    Status = models.CharField(max_length=33, choices=StatusChoices.choices, verbose_name="وضعیت")

    class Meta:
        verbose_name = "مشارکت"
        verbose_name_plural = "مشارکت"

    def __str__(self):
        return f"واریز {self.Amount} در {self.PurchaseTime}"
