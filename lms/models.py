from django.db import models
from django.urls import reverse
from inline_ordering.models import Orderable
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django_jalali.db.models import jDateTimeField
from django_jalali.db import models as jmodels
from ckeditor.fields import RichTextField
from django.conf import settings
# Create your models here.


def count_words_in_text(text_list, word_length):
    total_words = 0
    for current_text in text_list:
        total_words += len(current_text) / word_length
    return total_words


class Category(models.Model):
    name = models.CharField(max_length=202, null=False, blank=False, verbose_name="نام دسته بندی")
    slug = models.SlugField(unique=True, null=True, blank=False, verbose_name="لینک دسته بندی")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی دروس"

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("CourseCatPage", kwargs={"cat": self.slug, })


class Teacher(models.Model):
    name = models.CharField(max_length=202, null=False, blank=False, verbose_name="نام استاد")
    profile = models.ImageField(upload_to='files/avatar/teacher/', null=False, blank=False, verbose_name="تصویر استاد")
    birth = jmodels.jDateField(blank=True, default="", null=False, verbose_name="تاریخ تولد")
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
    title = models.CharField(max_length=202, null=False, blank=False, verbose_name="نام کلاس")
    slug = models.SlugField(unique=True, null=True, blank=False, verbose_name="آدرس کلاس")
    content = RichTextField(null=False, blank=False, verbose_name="توضیحات کلاس")
    cover = models.ImageField(upload_to='files/course/%Y/%m/', null=False, blank=False, verbose_name="تصویر کلاس")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE, verbose_name="دسته بندی")
    ostad = models.ForeignKey(Teacher, null=False, blank=False, on_delete=models.CASCADE, verbose_name="استاد")
    #
    CreatedDate = jmodels.jDateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    day = models.CharField(max_length=202, null=True, blank=True, verbose_name="تاریخ امتحان")
    ClassLength = models.CharField(max_length=110, default="10 هفته", null=True, blank=True, verbose_name="طول کلاس")
    #
    view_count = models.IntegerField(default=0, editable=False, verbose_name='بازدید ها')
    like_count = models.IntegerField(default=0, editable=False, verbose_name='پسند ها')

    @property
    def lesson_count(self):
        return Lesson.objects.filter(Course_id=self.id).count()

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
        return reverse("CourseView", kwargs={"slug": self.slug, "cat": self.category.slug, })

    def get_edit_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "files/lesson/{0}/{1}".format(instance.Course.slug, filename)


class Lesson(Orderable):
    title = models.CharField(max_length=202, null=False, blank=False, verbose_name="نام درس")
    content = RichTextField(null=False, blank=False, verbose_name="خلاصه توضیحات")
    file = models.FileField(upload_to=user_directory_path, null=False, blank=True, verbose_name="فایل درسی")
    lesson_length = models.CharField(max_length=202, blank=True, verbose_name="طول درس")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")
    Course = models.ForeignKey(Course, null=False, blank=False, on_delete=models.CASCADE, verbose_name="کلاس")
    view_count = models.IntegerField(default=0, editable=False, verbose_name='بازدید ها')
    like_count = models.IntegerField(default=0, editable=False, verbose_name='پسند ها')

    class Meta(Orderable.Meta):
        verbose_name = "درس"
        verbose_name_plural = "درس"

    @property
    def estimate_reading_time(self):
        total_words = count_words_in_text(self.content, 5)  # 5 is words length
        # natije_taghsim = total_words / 200  # 200 is wpm (word per min)
        # natije = "{: .2f}".format(round(natije_taghsim, 2))
        return round(total_words / 200)

    def save(self, *args, **kwargs):  # new
        if self.lesson_length == "":
            self.lesson_length = f"{self.estimate_reading_time} دقیقه"
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "LessonView",
            kwargs={"slug": self.Course.slug, "cat": self.Course.category.slug, "lid": self.id, }
        )
        # @todo lesson page

    def get_edit_url(self):
        return self.get_absolute_url()


class CourseRegister(models.Model):
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")
    Course = models.OneToOneField(Course, null=False, blank=False, on_delete=models.CASCADE, verbose_name="کلاس")
    Student = models.OneToOneField(to=settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE, verbose_name="دانشجو")

    class Meta:
        verbose_name = "ثبت نام در کلاس‌ها"
        verbose_name_plural = "ثبت نام در کلاس‌ها"
        unique_together = ("Course", "Student")

    def __str__(self):
        return f"عضویت {self.Student} در {self.Course}"
