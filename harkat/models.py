from ckeditor.fields import RichTextField
from django.db import models
from account.models import MadadKar
from django.urls import reverse
from django.utils.text import slugify
from django_jalali.db import models as jmodels
from location_field.models.plain import PlainLocationField
# Create your models here.


class CrowdCat(models.Model):
    Title = models.CharField(max_length=202, verbose_name="عنوان دسته‌بندی")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی کمک‌ها"

    def __str__(self):
        return self.Title

    def get_absolute_url(self):
        return reverse("harkat_cat", kwargs={"cid": self.id, })

    @property
    def statistics(self):
        result_total_count = CrowdFunding.objects.filter(Category_id=self.id).count()
        return result_total_count


class CrowdFunding(models.Model):
    StateChoices = (
        ('I', 'در حال جمع آوری کمک'),
        ('E', 'به نتیجه رسیده'),
        ('S', 'متوقف شده'),
    )
    Title = models.CharField(max_length=110, verbose_name="عنوان حرکت")
    Slug = models.SlugField(unique=True, verbose_name="لینک")
    Picture = models.ImageField(upload_to="files/jahad_activity/%Y/%m/", verbose_name="تصویر")
    Description = RichTextField(null=False, blank=False, verbose_name="توضیحات")
    Location = PlainLocationField(based_fields=['Slug'], zoom=9, blank=True, verbose_name='موقعیت مکانی')
    Category = models.ForeignKey(CrowdCat, on_delete=models.CASCADE, blank=True, null=True, verbose_name="دسته بندی")
    MadadKar = models.ForeignKey(MadadKar, on_delete=models.CASCADE, verbose_name="مددکار")
    Amount = models.BigIntegerField(verbose_name="کل مبلغ مورد نیاز")
    State = models.CharField(choices=StateChoices, default="I", max_length=20, verbose_name="وضعیت")

    class Meta:
        verbose_name = "تامین مالی حرکت جهادی"
        verbose_name_plural = "تامین مالی حرکت جهادی"

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
        result_total_amount = sum(
            [int(item.Amount) for item in Transaction.objects.filter(harkat=self, Status="S").all()]
        )
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
            value = int(int(jozea) * 100 / int(kol))
            if value < 101:
                return value
            else:
                return 100

    @property
    def percent_html(self):
        percent_html = f" <b>{self.percent}% </b> <div class='percent'>" \
                       f"<span class='its_ok' style=' width:{self.percent}%;'></span>" \
                       f"</div>"
        return percent_html


class Transaction(models.Model):
    StatusChoices = (
        ('X', 'نا موفق 🚫'),
        ('N', 'پرداخت نشده 🔄'),
        ('S', 'پرداخت شده ✅'),
    )

    harkat = models.ForeignKey(CrowdFunding, on_delete=models.CASCADE, verbose_name="حرکت")

    # Purchaser = models.ForeignKey(UserDetail, on_delete=models.CASCADE, verbose_name="خریدار")

    Purchaser = models.CharField(max_length=202, blank=True, verbose_name="نام واریز کننده")

    PurchaserTel = models.CharField(max_length=12, blank=True, verbose_name="شماره تماس واریز کننده")

    PurchaserIP = models.CharField(max_length=16, editable=False, verbose_name="آیپی خریدار")

    PurchaseID = models.CharField(blank=True, max_length=202, verbose_name="شناسه واریز")

    PurchaseTime = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ واریز")

    Amount = models.CharField(max_length=202, verbose_name="مبلغ")

    Description = models.TextField(blank=True, verbose_name="توضیحات")

    Status = models.CharField(max_length=33, choices=StatusChoices, verbose_name="وضعیت")

    class Meta:
        verbose_name = "مشارکت"
        verbose_name_plural = "مشارکت"

    @property
    def status_name(self):
        name_val = dict(self.StatusChoices).get(self.Status)
        return name_val

    def __str__(self):
        return f"واریز {self.Amount} « برای {self.harkat}»"
