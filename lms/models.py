import home
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django_jalali.db.models import jDateTimeField
from django_jalali.db import models as jmodels
from ckeditor.fields import RichTextField
# Create your models here.


class Teacher(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name="نام استاد")
    profile = models.ImageField(upload_to='files/avatar/teacher/', null=False, blank=False, verbose_name="تصویر استاد")
    birth = jmodels.jDateField(blank=True, verbose_name="تاریخ تولد")
    resume = RichTextField(blank=True, verbose_name="رزومه")

    class Meta:
        verbose_name = "استاد"
        verbose_name_plural = "استاد"

    def __str__(self):
        return f" استاد {self.name}"

    @property
    def thumbnail_preview(self):
        if self.profile:
            return mark_safe(
                '<img src="{}" style="object-fit:contain; height:auto; max-height:110px; " width="110" />'.format(
                    self.profile.url))
        return ""


class Course(models.Model):
    PayeChoices = (
        ('0', 'دهم'),
        ('1', 'یازدهم'),
        ('2', 'دوازدهم'),
    )
    title = models.CharField(max_length=202, null=False, blank=False, verbose_name="نام کلاس")
    slug = models.SlugField(unique=True, null=True, blank=False, verbose_name="آدرس کلاس")
    content = RichTextField(null=False, blank=False, verbose_name="خلاصه توضیحات")
    cover = models.ImageField(upload_to='files/course/', null=False, blank=False, verbose_name="تصویر کلاس")
    ostad = models.ForeignKey(Teacher, null=False, blank=False, on_delete=models.CASCADE, verbose_name="استاد")
    #
    CreatedDate = jmodels.jDateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    paye = models.CharField(max_length=1, choices=PayeChoices, null=True, blank=True, verbose_name="پایه کلاس")
    day = models.CharField(max_length=202, null=True, blank=True, verbose_name="روز کلاس")
    ClassLength = models.CharField(max_length=110, default="10 هفته", null=True, blank=True, verbose_name="طول کلاس")
    #
    view_count = models.IntegerField(default=0, editable=False, verbose_name='بازدید ها')
    like_count = models.IntegerField(default=0, editable=False, verbose_name='پسند ها')

    class Meta:
        verbose_name = "کلاس درس"
        verbose_name_plural = "کلاس درس"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def jpublish(self):
        return jDateTimeField(self.CreatedDate)

    def get_absolute_url(self):
        return f"course/lesson/{self.slug}"
        # return reverse(f"course/lesson/{self.slug}")


class Section(models.Model):
    Course = models.OneToOneField(Course, on_delete=models.CASCADE, verbose_name="کلاس درس")
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name="نام بخش")

    class Meta:
        verbose_name = "فصل درسی"
        verbose_name_plural = "فصل درسی"


class Lesson(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name="نام کلاس")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=False, blank=False, verbose_name="نام بخش")
    content = RichTextField(null=False, blank=False, verbose_name="خلاصه توضیحات")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")
    view_count = models.IntegerField(default=0, editable=False, verbose_name='بازدید ها')
    like_count = models.IntegerField(default=0, editable=False, verbose_name='پسند ها')

    class Meta:
        verbose_name = "دروس"
        verbose_name_plural = "دروس"
