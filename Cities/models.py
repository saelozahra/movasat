from django.db import models


class Provinces(models.Model):
    Name = models.CharField(max_length=110, verbose_name="نام")

    class Meta:
        verbose_name = "استان"
        verbose_name_plural = "استان ها"

    def __str__(self):
        return self.Name


class City(models.Model):
    Provinces = models.ForeignKey(Provinces, on_delete=models.CASCADE, verbose_name="استان")
    Name = models.CharField(max_length=110, verbose_name="نام")

    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهر ها"

    def __str__(self):
        return self.Name
