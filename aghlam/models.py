from django.db import models
# Create your models here.


class Bohran(models.Model):
    name = models.CharField(max_length=202, null=False, blank=False, verbose_name="نام بحران")

    class Meta:
        verbose_name = "بحران"
        verbose_name_plural = "بحران"


class AghlamKomaki(models.Model):
    name = models.CharField(max_length=202, null=False, blank=False, verbose_name="نام اقلام")

    class Meta:
        verbose_name = "اقلام"
        verbose_name_plural = "اقلام"
