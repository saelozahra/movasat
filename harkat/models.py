from ckeditor.fields import RichTextField
from django.db import models
from account.models import MadadKar, UserDetail
from django.urls import reverse
from django.utils.text import slugify
from django_jalali.db import models as jmodels
# Create your models here.


class Harkat(models.Model):
    StateChoices = (
        ('I', 'در حال جمع آوری کمک'),
        ('E', 'به نتیجه رسیده'),
        ('S', 'متوقف شده'),
    )
    Title = models.CharField(max_length=110, verbose_name="عنوان حرکت")
    Slug = models.SlugField(unique=True, verbose_name="لینک")
    Picture = models.ImageField(upload_to="files/jahad_activity/", verbose_name="تصویر")
    Description = RichTextField(null=False, blank=False, verbose_name="توضیحات")
    MadadKar = models.ForeignKey(MadadKar, on_delete=models.CASCADE, verbose_name="مددکار")
    Amount = models.BigIntegerField(verbose_name="کل مبلغ مورد نیاز")
    State = models.CharField(choices=StateChoices, default="I", max_length=20, verbose_name="وضعیت")

    class Meta:
        verbose_name = "تامین مالی حرکت"
        verbose_name_plural = "تامین مالی حرکت"

    def __str__(self):
        return f"تامین {self.Amount:,} تومان ، برای {self.Title} توسط {self.MadadKar}"

    def save(self, *args, **kwargs):  # new
        if not self.Slug:
            self.slug = slugify(self.Title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("harkat_single", kwargs={"slug": self.Slug, "jahadi": self.MadadKar.user.username, })

    @property
    def total_amount(self):
        result_total_amount = sum([int(item.Amount) for item in Transaction.objects.filter(harkat=self).all()])
        return result_total_amount

    @property
    def percent(self):
        kol = self.Amount
        jozea = self.total_amount
        if kol == 0:
            return 0
        elif kol == jozea:
            return 100
        else:
            return int(int(jozea) * 100 / int(kol))

    @property
    def percent_html(self):
        percent_html = f" <b>{self.percent}% </b> <div class='percent'>" \
                       f"<span class='its_ok' style=' width:{self.percent}%;'></span>" \
                       f"</div>"
        return percent_html


class Transaction(models.Model):
    StatusChoices = (
        ('X', 'نا موفق'),
        ('N', 'پرداخت نشده'),
        ('S', 'پرداخت شده'),
    )

    harkat = models.ForeignKey(Harkat, on_delete=models.CASCADE, verbose_name="حرکت")

    # Purchaser = models.ForeignKey(UserDetail, on_delete=models.CASCADE, verbose_name="خریدار")

    Purchaser = models.CharField(max_length=202, blank=True, verbose_name="نام واریز کننده")

    PurchaserTel = models.CharField(max_length=12, blank=True, verbose_name="شماره تماس واریز کننده")

    PurchaserIP = models.CharField(max_length=16, editable=False, verbose_name="آیپی خریدار")

    PurchaseID = models.CharField(max_length=202, verbose_name="شناسه واریز")

    PurchaseTime = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ واریز")

    Amount = models.CharField(max_length=200, verbose_name="مبلغ")

    Status = models.CharField(max_length=33, choices=StatusChoices, verbose_name="وضعیت")

    class Meta:
        verbose_name = "مشارکت"
        verbose_name_plural = "مشارکت"

    def __str__(self):
        return f"واریز {self.Amount} « برای {self.harkat}»"
