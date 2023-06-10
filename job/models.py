from ckeditor.fields import RichTextField
from colorfield.fields import ColorField
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

class Job(models.Model):
    name = models.CharField(max_length=202, blank=False, null=False, verbose_name="نام کسب و کار")
    description = RichTextField(blank=True, verbose_name="توضیحات")
    JobCat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="دسته بندی")
    photo = models.ImageField(upload_to='files/job/%Y/%m/', null=False, blank=False, verbose_name="تصویر")
    thumbnail = models.ImageField(upload_to='files/job/%Y/%m/', editable=False, blank=True, verbose_name='تصویرک')
    date = jmodels.jDateField(blank=True, auto_created=True, verbose_name="تاریخ")

    def save(self, *args, **kwargs):
        output_size = (313, 313)
        output_thumb = BytesIO()

        img = Image.open(self.photo)
        img_name = self.photo.name.split('.')[0]

        if img.height > 313 or img.width > 313:
            img.thumbnail(output_size)
            img.save(output_thumb, format='JPEG', quality=90)

        self.thumbnail = InMemoryUploadedFile(output_thumb, 'ImageField', f"{img_name}_thumb.jpg", 'image/jpeg',
                                               sys.getsizeof(output_thumb), None)
        return super().save(*args, **kwargs)
