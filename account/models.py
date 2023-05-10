from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from location_field.models.plain import PlainLocationField
from Cities.models import *


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
    City = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="شهر")
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


class MadadKar(models.Model):
    TYPE_CHOICES = (
        ('j', 'گروه جهادی'),
        ('k', 'موسسه خیریه'),
        ('n', 'سازمان مردم نهاد'),
    )
    GroupType = models.CharField(choices=TYPE_CHOICES, max_length=1, verbose_name="نوع")
    Name = models.CharField(max_length=110, verbose_name="نام")
    RegisterCode = models.PositiveIntegerField(verbose_name="کد ثبت موسسه",
                    help_text="توجه کنید که تمامی حقوق مربوط به حرکت های ثبتی توسط شما متوجه این موسسه خواهد بود")
    Cover = models.ImageField(verbose_name="کاور")
    Avatar = models.ImageField(verbose_name="آواتار")
    Bio = models.TextField(verbose_name="توضیحات")
    Url = models.URLField(verbose_name="وبسایت", blank=True)
    Number = models.CharField(max_length=11, verbose_name="شماره تلفن")
    Eita = models.URLField(verbose_name="لینک صفحه در ایتا", blank=True)
    Rubika = models.URLField(verbose_name="لینک صفحه در روبیکا", blank=True)
    Bale = models.URLField(verbose_name="لینک صفحه در بله", blank=True)
    City = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="شهر")
    Location = PlainLocationField(default='29.5,52.5', zoom=4, blank=True, verbose_name='موقعیت مکانی')
    Address = models.TextField(verbose_name="آدرس")

    class Meta:
        verbose_name = "مددکار"
        verbose_name_plural = "مددکار ها"

    def __str__(self):
        return self.Name


