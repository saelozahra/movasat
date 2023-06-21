import sys
from PIL import Image
from io import BytesIO

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django_jalali.db import models as jmodels
from django.urls import reverse
from harkat.models import Project
from ckeditor.fields import RichTextField


# Create your models here.


class Forum(models.Model):
    title = models.CharField(max_length=202, null=False, verbose_name="عنوان چالش")
    description = RichTextField(blank=False, null=False, verbose_name="توضیحات چالش")
    cover = models.ImageField(blank=True, upload_to="files/challenge/%Y/%m/", verbose_name="تصویر")
    thumbnail = models.ImageField(upload_to='files/challenge/%Y/%m/', editable=False, blank=True, verbose_name='تصویرک')
    file = models.FileField(blank=True, upload_to="files/challenge/%Y/%m/", verbose_name="فایل")
    RelatedProject = models.ForeignKey(Project, blank=True, on_delete=models.DO_NOTHING, verbose_name="پروژه مربوطه")
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name="مطرح کننده")
    date = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ")

    class Meta:
        verbose_name = "چالش"
        verbose_name_plural = "چالش"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("show_forum", kwargs={"fid": self.id, })

    def save(self, *args, **kwargs):
        output_size = (313, 313)
        output_thumb = BytesIO()

        img = Image.open(self.cover)
        img_name = self.cover.name.split('.')[0]

        if img.height > 313 or img.width > 313:
            img.thumbnail(output_size)
            img.save(output_thumb, format='JPEG', quality=90)

        self.thumbnail = InMemoryUploadedFile(output_thumb, 'ImageField', f"{img_name}_thumb.jpg", 'image/jpeg',
                                              sys.getsizeof(output_thumb), None)
        return super().save(*args, **kwargs)


class Response(models.Model):
    description = RichTextField(blank=False, null=False, verbose_name="توضیحات چالش")
    file = models.FileField(blank=True, upload_to="files/challenge/%Y/%m/", verbose_name="فایل")
    writer = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name="نویسنده")
    RelatedForum = models.ForeignKey(Forum, blank=True, on_delete=models.DO_NOTHING, verbose_name="پروژه مربوطه")
    date = jmodels.jDateTimeField(auto_now=True, verbose_name="زمان")

    class Meta:
        verbose_name = "پاسخ"
        verbose_name_plural = "پاسخ"

    def __str__(self):
        return f"پاسخ {self.id}، {self.writer.get_full_name()} به {self.RelatedForum}"


class Divar(models.Model):
    StatusChoices = (
        (1, 'آزاد ✅'),
        (2, 'در حال استفاده 🔄'),
        (3, 'امانت داده شده 💠'),
    )

    TypeChoices = (
        (True, 'امانت دادن'),
        (False, 'نیازمندی'),
    )

    Type = models.BooleanField(choices=TypeChoices, verbose_name="نوع آگهی", default=True,
                               help_text="به این کالا برا کار خیرتون نیاز دارید؟ یا میخواید به یکی دیگه امانتش بدید؟")
    Name = models.CharField(max_length=202, null=False, verbose_name="نام")
    Description = RichTextField(null=False, verbose_name="متن")
    Picture = models.ImageField(blank=True, upload_to="files/divar/%Y/%m/", verbose_name="تصویر")
    Thumbnail = models.ImageField(upload_to='files/divar/%Y/%m/', editable=False, blank=True, verbose_name='تصویرک')
    SubmitDate = jmodels.jDateTimeField(auto_now=True, verbose_name="زمان ثبت")
    RelatedProject = models.ForeignKey(Project, blank=True, on_delete=models.DO_NOTHING, verbose_name="پروژه مربوطه")
    Warranty = models.CharField(max_length=313, blank=True, help_text="برای ضمانت چی میخواین ؟", verbose_name="ضمانت")
    Admin = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="آگهی دهنده")
    Status = models.PositiveSmallIntegerField(choices=StatusChoices,default=1, verbose_name="وضعیت")

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = "دیوار مهربانی"
        verbose_name_plural = "دیوار مهربانی"

    def save(self, *args, **kwargs):
        output_size = (444, 313)
        output_thumb = BytesIO()

        img = Image.open(self.Picture)
        img_name = self.Picture.name.split('.')[0]

        if img.height > 444 or img.width > 313:
            img.thumbnail(output_size)
            img.save(output_thumb, format='JPEG', quality=90)

        self.Thumbnail = InMemoryUploadedFile(output_thumb, 'ImageField', f"{img_name}_thumb.jpg", 'image/jpeg',
                                              sys.getsizeof(output_thumb), None)
        return super().save(*args, **kwargs)

    @property
    def type_value(self):
        type_val = dict(self.TypeChoices).get(self.Type)
        return type_val

    def get_absolute_url(self):
        return reverse("show_divar", kwargs={"did": self.id, })
