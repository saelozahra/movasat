from ckeditor.fields import RichTextField
from django.db import models

# Create your models here.


class Box(models.Model):
    title = models.CharField(max_length=202, null=False, blank=False, verbose_name="عنوان")
    location = models.SlugField(unique=True, verbose_name="محل قرارگیری")
    photo = models.ImageField(upload_to='files/', null=True, blank=True, verbose_name="تصویر")
    content = RichTextField(blank=True, verbose_name="محتوا")

    class Meta:
        verbose_name = "باکس‌ها"
        verbose_name_plural = "باکس‌ها"

    def __str__(self):
        return self.title
