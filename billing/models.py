from django.db import models

from user.models import TgUser

BALANCE_TRANSACTION_TYPES = (
    (1, "Kirim"),
    (2, "Ariza uchun to'lov"),
    (4, "Balansdan yechish")
)


class BalanceTransaction(models.Model):
    user = models.ForeignKey(TgUser, on_delete=models.PROTECT,
                             verbose_name="Foydalanuvchi")  # order
    transaction_id = models.CharField(max_length=255, blank=True)
    time_millisecond = models.CharField(max_length=255, blank=True,
                                        verbose_name="API kelgan vaqt (format:millisecond)")
    time_datetime = models.DateTimeField(null=True, blank=True)
    perform_time = models.DateTimeField(null=True, blank=True, verbose_name="Tasdiqlangan vaqti:")
    create_time = models.DateTimeField(null=True, blank=True, verbose_name="Yaratilgan vaqti:")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    cancel_time = models.DateTimeField(null=True, blank=True)
    error = models.TextField(default='Aniqlanmadi!', blank=True, null=True)
    type = models.IntegerField(default=1, choices=BALANCE_TRANSACTION_TYPES, verbose_name="Turi")
    amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Summa",
                                 help_text="XXX.XX som",
                                 default="0")
    reason = models.CharField(max_length=300, verbose_name="Tranzaksiya sababi (izoh)", blank=True,
                              null=True)

    TRANSACTION_STATUS = (
        (0, "Не существует"),
        (1, "Создан"),
        (2, "Оплачен"),
        (-1, "Отменен"),
        (-2, "Отменена после завершения")
    )
    state = models.IntegerField(default=1, choices=TRANSACTION_STATUS)
    balance_updated = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Транзаксия"
        verbose_name_plural = "Транзаксиялар"

    def __str__(self):
        return str(self.transaction_id)

    def clean(self):
        b = TgUser.objects.get(tg_id=self.user.tg_id)
        if self.type == 1 and self.state == 3:
            b.balance = b.balance + self.amount
            b.save()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
