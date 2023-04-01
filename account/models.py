from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from location_field.models.plain import PlainLocationField
# Create your models here.


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.SmallIntegerField(default=0, editable=False)
    phone = models.CharField(max_length=11, verbose_name="شماره تماس")
    birth = jmodels.jDateField(blank=True, null=True, verbose_name="تاریخ تولد")
    father = models.CharField(max_length=110, blank=True, verbose_name="نام پدر")
    parent_tel = models.CharField(max_length=11, blank=True, verbose_name="شماره تماس والدین")

    class Meta:
        verbose_name = "اطلاعات کاربری"
        verbose_name_plural = "اطلاعات کاربری"


class MadadJoo(models.Model):
    name = models.CharField(max_length=202, null=False, blank=False, verbose_name="نام مددجو")
    tel = models.CharField(max_length=11, null=False, blank=False, verbose_name="شماره تماس")
    melli = models.CharField(max_length=10, unique=True, null=False, blank=False, verbose_name="کد ملی")
    address = models.CharField(max_length=444, null=False, blank=False, verbose_name="نشانی منزل")
    postalcode = models.CharField(max_length=12, unique=True, null=False, blank=False, verbose_name="کد پستی")
    Location = PlainLocationField(default='29.5,52.5', zoom=4, blank=True, verbose_name='موقعیت مکانی')
    khanevar = models.PositiveIntegerField(default=1, verbose_name="جمعیت خانوار")
    # aghlam = models.ForeignKey(AghlamKomaki, on_delete=models.CASCADE, verbose_name="اقلام کمکی")
    operator = models.ForeignKey(UserDetail, on_delete=models.CASCADE, verbose_name="اهدا کننده")
    moarefiNiazmand = models.BooleanField(default=False, verbose_name="معرفی به عنوان نیازمند")
    RegisterDate = jmodels.jDateTimeField(auto_created=True, verbose_name="تاریخ ثبت نام")
    submitbyapp = models.BooleanField(default=True, verbose_name="ثبت شده توسط اپلیکیشن")

    class Meta:
        unique_together = ('melli', 'postalcode')
        verbose_name = "مددجو"
        verbose_name_plural = "مددجو"
