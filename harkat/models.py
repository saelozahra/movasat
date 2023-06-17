from ckeditor.fields import RichTextField
from colorfield.fields import ColorField
from django.db import models
from account.models import MadadKar
from django.urls import reverse
from django.utils.text import slugify
from django_jalali.db import models as jmodels
from location_field.models.plain import PlainLocationField
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
# Create your models here.


class Category(models.Model):
    TypeSelect = [
        (1, "هارمونی بنفش", ),
        (2, "هارمونی آبی", ),
        (3, "هارمونی سبز", ),
    ]
    name = models.CharField(max_length=202, null=False, blank=False, verbose_name="نام دسته بندی")
    CType = models.PositiveSmallIntegerField(default=1, choices=TypeSelect, blank=False, verbose_name="تم رنگی")
    icon = models.ImageField(upload_to='files/project/cat/', blank=True, verbose_name="آیکون")
    color = ColorField(image_field="icon", blank=False, verbose_name="رنگ")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("harkat_cat", kwargs={"cid": self.id, })

    @property
    def statistics(self):
        cf_num = CrowdFunding.objects.filter(Category_id=self.id).count()
        p_num = Project.objects.filter(ProjectCat_id=self.id).count()
        result_total_count = cf_num + p_num
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
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, verbose_name="دسته بندی")
    MadadKar = models.ForeignKey(MadadKar, on_delete=models.CASCADE, verbose_name="مددکار")
    Amount = models.BigIntegerField(verbose_name="کل مبلغ مورد نیاز")
    date = jmodels.jDateField(blank=True, auto_now=True, verbose_name="تاریخ")
    State = models.CharField(choices=StateChoices, default="I", max_length=20, verbose_name="وضعیت")
    view_count = models.IntegerField(default=0, editable=False, verbose_name='بازدید ها')
    like_count = models.IntegerField(default=0, editable=False, verbose_name='پسند ها')

    class Meta:
        verbose_name = "تامین مالی حرکت جهادی"
        verbose_name_plural = "تامین مالی حرکت جهادی"

    def __str__(self):
        return f"تامین {self.Amount:,} تومان ، برای {self.Title} توسط {self.MadadKar}"

    def save(self, *args, **kwargs):  # new
        if not self.Slug:
            self.slug = slugify(self.Title)
        Project.objects.create(
            madadkar=self.MadadKar,
            ProjectCat=self.Category,
            name=self.Title,
            photo=self.Picture,
            date=self.date,
            description=self.Description,
        )
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


class Project(models.Model):
    madadkar = models.ForeignKey(MadadKar, on_delete=models.CASCADE, verbose_name="مددکار")
    ProjectCat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="دسته بندی")
    name = models.CharField(max_length=202, null=False, blank=False, verbose_name="نام پروژه")
    photo = models.ImageField(upload_to='files/project/', null=False, blank=False, verbose_name="تصویر")
    thumbnail = models.ImageField(upload_to='files/project/thumb', editable=False, blank=True, verbose_name='تصویرک')
    date = jmodels.jDateField(blank=True, verbose_name="تاریخ")
    description = RichTextField(blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه"

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

    def __str__(self):
        return self.name
