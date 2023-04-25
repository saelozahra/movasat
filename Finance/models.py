from django.db import models
from account.models import UserDetail


class HarekatPay(models.Model):

    class StatusChoices(models.TextChoices):
        X = 'نا موفق'
        N = 'پرداخت نشده'
        S = 'پرداخت شده'

    # harekat = models.ForeignKey(Harekat, on_delete=models.CASCADE, verbose_name="حرکت")

    Purchaser = models.ForeignKey(UserDetail, on_delete=models.CASCADE, verbose_name="خریدار")

    Status = models.CharField(max_length=200, choices=StatusChoices.choices, verbose_name="وضعیت")

    PurchaseID = models.CharField(max_length=200, verbose_name="شناسه واریز")

    PurchaseTime = models.CharField(max_length=200, verbose_name="تاریخ واریز")

    Amount = models.CharField(max_length=200, verbose_name="مبلغ")

    Wage = models.CharField(max_length=200, verbose_name="کارمزد")

    class Meta:
        verbose_name = "خرید در حرکت"
        verbose_name_plural = "خرید ها در حرکت"

    def __str__(self):
        return " حرکت " \
            + " : " \
            + " تاریخ واریز : " \
            + self.PurchaseTime
