from django.db import models
from django.contrib.auth.models import User
from account.models import MadadKar
from django_jalali.db import models as jmodels
from Cities.models import City
from location_field.models.plain import PlainLocationField


# Create your models here.


class MadadJoo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tel = models.CharField(max_length=11, null=False, blank=False, verbose_name="شماره تماس")
    melli = models.CharField(max_length=10, unique=True, null=False, blank=False, verbose_name="کد ملی")
    City = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="شهر")
    address = models.CharField(max_length=444, null=False, blank=False, verbose_name="نشانی منزل")
    postalcode = models.CharField(max_length=12, unique=True, null=False, blank=False, verbose_name="کد پستی")
    Location = PlainLocationField(default='29.5,52.5', zoom=4, blank=True, verbose_name='موقعیت مکانی')
    khanevar = models.PositiveIntegerField(default=1, verbose_name="جمعیت خانوار")
    # aghlam = models.ForeignKey(AghlamKomaki, on_delete=models.CASCADE, verbose_name="اقلام کمکی")
    # operator = models.ForeignKey(UserDetail, on_delete=models.CASCADE, verbose_name="اهدا کننده")
    moarefiNiazmand = models.BooleanField(default=False, verbose_name="معرفی به عنوان نیازمند")
    RegisterDate = jmodels.jDateTimeField(auto_created=True, verbose_name="تاریخ ثبت نام")
    submitbyapp = models.BooleanField(default=True, verbose_name="ثبت شده توسط اپلیکیشن")

    class Meta:
        unique_together = ('melli', 'postalcode')
        verbose_name = "مددجو"
        verbose_name_plural = "مددجو"


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
