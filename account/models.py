from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse
from django_jalali.db import models as jmodels
from job.models import Skills
from location_field.models.plain import PlainLocationField
from Cities.models import City


class UserDetail(AbstractUser):
    otp = models.SmallIntegerField(default=0, editable=False)
    tel = models.CharField(max_length=11, null=False, blank=False, verbose_name="شماره تماس")
    Avatar = models.ImageField(upload_to="files/avatar/", verbose_name="آواتار")
    melli = models.CharField(max_length=10, unique=True, null=False, blank=False, verbose_name="کد ملی")
    City = models.ForeignKey(City, on_delete=models.CASCADE, null=True, verbose_name="شهر")
    birth = jmodels.jDateField(blank=True, null=True, verbose_name="تاریخ تولد")
    skills = models.ForeignKey(Skills, on_delete=models.CASCADE, blank=True, null=True, verbose_name="تخصص ها")
    is_job_finder = models.BooleanField(default=False, verbose_name="در جستجوی کار")

    class Meta:
        verbose_name = "اطلاعات کاربری"
        verbose_name_plural = "اطلاعات کاربری"


class MadadKar(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="حساب کاربری")
    TYPE_CHOICES = (
        ('j', 'گروه جهادی'),
        ('k', 'موسسه خیریه'),
        ('n', 'سازمان مردم نهاد'),
    )
    GroupType = models.CharField(choices=TYPE_CHOICES, max_length=1, verbose_name="نوع")
    Name = models.CharField(max_length=110, verbose_name="نام موسسه")
    RegisterCode = models.PositiveIntegerField(verbose_name="کد ثبت موسسه",
                    help_text="توجه کنید که تمامی حقوق مربوط به حرکت های ثبتی توسط شما متوجه این موسسه خواهد بود")
    Cover = models.ImageField(upload_to="files/cover/", verbose_name="کاور")
    Avatar = models.ImageField(upload_to="files/avatar/", verbose_name="آواتار")
    Bio = models.TextField(verbose_name="توضیحات")
    City = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="شهر")
    Location = PlainLocationField(default='29.5,52.5', zoom=4, blank=True, verbose_name='موقعیت مکانی')
    Address = models.TextField(verbose_name="آدرس")
    Url = models.URLField(verbose_name="وبسایت", blank=True)
    Tel = models.CharField(max_length=11, verbose_name="شماره تلفن")
    Eita = models.URLField(verbose_name="لینک صفحه در ایتا", blank=True)
    Rubika = models.URLField(verbose_name="لینک صفحه در روبیکا", blank=True)
    Bale = models.URLField(verbose_name="لینک صفحه در بله", blank=True)

    class Meta:
        verbose_name = "مددکار"
        verbose_name_plural = "مددکار ها"

    def __str__(self):
        name_val = dict(self.TYPE_CHOICES).get(self.GroupType)
        return f"{name_val}  «{self.Name}»"

    def get_absolute_url(self):
        # return reverse("get_profile", kwargs={"user": self.user.username, })
        return reverse("get_profile", kwargs={"user": UserDetail.objects.get(id=self.user_id).username, })

    def get_edit_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))
