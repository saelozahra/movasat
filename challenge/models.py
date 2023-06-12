from urllib import request

import requests
from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse
from harkat.models import Project
from ckeditor.fields import RichTextField


# Create your models here.


class Forum(models.Model):
    title = models.CharField(max_length=202, null=False, verbose_name="عنوان چالش")
    description = RichTextField(blank=False, null=False, verbose_name="توضیحات چالش")
    cover = models.ImageField(blank=True, upload_to="files/challenge/%Y/%m/", verbose_name="تصویر")
    file = models.FileField(blank=True, upload_to="files/challenge/%Y/%m/", verbose_name="فایل")
    RelatedProject = models.ForeignKey(Project, blank=True, on_delete=models.DO_NOTHING, verbose_name="پروژه مربوطه")
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="مطرح کننده")
    date = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ")

    class Meta:
        verbose_name = "چالش"
        verbose_name_plural = "چالش"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("show_forum", kwargs={"fid": self.id, })


class Response(models.Model):
    description = RichTextField(blank=False, null=False, verbose_name="توضیحات چالش")
    file = models.FileField(blank=True, upload_to="files/challenge/%Y/%m/", verbose_name="فایل")
    writer = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="نویسنده")
    RelatedForum = models.ForeignKey(Forum, blank=True, on_delete=models.DO_NOTHING, verbose_name="پروژه مربوطه")
    date = jmodels.jDateTimeField(auto_now=True, verbose_name="زمان")

    class Meta:
        verbose_name = "پاسخ"
        verbose_name_plural = "پاسخ"

    def __str__(self):
        return f"پاسخ {self.id}، {self.writer.get_full_name()} به {self.RelatedForum}"

    # def save(self, *args, **kwargs):
    #     if self.writer is None:
    #     return super().save(*args, **kwargs)
