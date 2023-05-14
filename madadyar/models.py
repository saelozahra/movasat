from django.db import models
from account.models import MadadKar, MadadJoo
from django_jalali.db import models as jmodels
# Create your models here.


class Bohran(models.Model):
    name = models.CharField(max_length=202, null=False, blank=False, verbose_name="نام بحران")

    class Meta:
        verbose_name = "بحران"
        verbose_name_plural = "بحران"

    def __str__(self):
        return self.name


class Aghlam(models.Model):
    name = models.CharField(max_length=202, null=False, blank=False, verbose_name="نام اقلام")

    class Meta:
        verbose_name = "اقلام"
        verbose_name_plural = "اقلام"

    def __str__(self):
        return self.name


class JahadActivity(models.Model):
    MadadKar = models.ForeignKey(MadadKar, on_delete=models.CASCADE, verbose_name="مددکار")
    aghlam = models.ForeignKey(Aghlam, on_delete=models.CASCADE, verbose_name="اقلام")
    MadadJoo = models.ForeignKey(MadadJoo, on_delete=models.CASCADE, verbose_name="مددجو")
    Description = models.TextField(verbose_name="توضیحات")
    Amount = models.BigIntegerField(verbose_name="مبلغ")
    TotalAmount = models.BigIntegerField(blank=True, verbose_name="حدود قیمت")
    Zaman = jmodels.jDateTimeField(auto_now_add=True, verbose_name="زمان ساخت")

    class Meta:
        verbose_name = "کمک رسانی"
        verbose_name_plural = "کمک رسانی"

    def __str__(self):
        return f"اهدای {self.aghlam} به {self.MadadJoo} در {self.Zaman}"
