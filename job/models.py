from ckeditor.fields import RichTextField
from colorfield.fields import ColorField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_jalali.db import models as jmodels
from location_field.models.plain import PlainLocationField
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.


class Skills(models.Model):
    name = models.CharField(max_length=202, null=False, blank=False, verbose_name="نام تخصص")
    slug = models.SlugField(unique=True, verbose_name="لینک")
    icon = models.ImageField(upload_to='files/job/skill/', blank=True, verbose_name="آیکون")
    color = ColorField(image_field="icon", blank=True, verbose_name="رنگ")
    view_count = models.IntegerField(default=0, editable=False, verbose_name='بازدید ها')
    like_count = models.IntegerField(default=0, editable=False, verbose_name='پسند ها')

    class Meta:
        verbose_name = "تخصص ها"
        verbose_name_plural = "تخصص ها"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    @property
    def statistics(self):
        return Job.objects.filter(skills=self).count()


class Category(models.Model):
    name = models.CharField(max_length=202, null=False, blank=False, verbose_name="نام دسته بندی")
    slug = models.SlugField(unique=True, verbose_name="لینک")
    icon = models.ImageField(upload_to='files/job/cat/', blank=True, verbose_name="آیکون")
    color = ColorField(image_field="icon", blank=False, verbose_name="رنگ")
    view_count = models.IntegerField(default=0, editable=False, verbose_name='بازدید ها')
    like_count = models.IntegerField(default=0, editable=False, verbose_name='پسند ها')

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("job_cat", kwargs={"jcat": self.slug, })

    def get_edit_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    @property
    def statistics(self):
        result_total_count = Job.objects.filter(JobCat_id=self.id).count()
        return result_total_count


class Job(models.Model):
    name = models.CharField(max_length=202, blank=False, null=False, verbose_name="نام کسب و کار")
    description = RichTextField(blank=True, verbose_name="توضیحات")
    JobCat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="دسته بندی")
    need = models.PositiveSmallIntegerField(blank=False, null=False, default=0, verbose_name="تعداد افراد مورد نیاز")
    skills = models.ManyToManyField(Skills, verbose_name="تخصص های مورد نیاز")
    owner = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_owner", verbose_name="مدیر این کسب و کار")
    photo = models.ImageField(upload_to='files/job/%Y/%m/', null=False, blank=False, verbose_name="تصویر")
    thumbnail = models.ImageField(upload_to='files/job/%Y/%m/', editable=False, blank=True, verbose_name='تصویرک')
    address = models.TextField(blank=True, default="", verbose_name="نشانی کسب و کار")
    location = PlainLocationField(default='29.5,52.5', zoom=4, blank=True, verbose_name='موقعیت مکانی')
    date = jmodels.jDateField(blank=True, auto_now_add=True, verbose_name="تاریخ درخواست")
    view_count = models.IntegerField(default=0, editable=False, verbose_name='بازدید ها')
    like_count = models.IntegerField(default=0, editable=False, verbose_name='پسند ها')

    def save(self, *args, **kwargs):
        output_thumb = BytesIO()

        img = Image.open(self.photo)
        img_name = self.photo.name.split('.')[0]

        if img.height > 313 or img.width > 313:
            img.thumbnail((313, 313))
            img.save(output_thumb, format='JPEG', quality=90)

        self.thumbnail = InMemoryUploadedFile(output_thumb, 'ImageField', f"{img_name}_thumb.jpg", 'image/jpeg',
                                              sys.getsizeof(output_thumb), None)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "کسب و کار"
        verbose_name_plural = "کسب و کار"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("single_job", kwargs={"jowner": self.owner, "jcat": self.JobCat.slug, "jid": self.id, })

    def get_edit_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))
