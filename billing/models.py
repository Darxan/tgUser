from django.db import models

from telegram.user.models import TgUser


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=255, blank=True)
    time_millisecond = models.CharField(max_length=255, blank=True, verbose_name="API kelgan vaqt (format:millisecond)")
    time_datetime = models.DateTimeField(null=True, blank=True)
    perform_time = models.DateTimeField(null=True, blank=True, verbose_name="Tasdiqlangan vaqti:")
    create_time = models.DateTimeField(null=True, blank=True, verbose_name="Yaratilgan vaqti:")
    cancel_time = models.DateTimeField(null=True, blank=True)
    error = models.TextField(default='Aniqlanmadi!', blank=True, null=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Summa", help_text="XXX.XX som",
                                 default=0.0)
    user = models.ForeignKey(TgUser, on_delete=models.SET_NULL, blank=True, null=True)
    reason = models.CharField(max_length=300, verbose_name="Tranzaksiya sababi (izoh)", blank=True, null=True)
    TRANSACTION_STATUS = (
        (0, _("Не существует")),
        (1, _("Транзакция создан")),
        (2, _("Транзакция оплачен")),
        (-1, _("Транзакция отменен")),
        (-2, _("Отменена после завершения"))
    )
    state = models.IntegerField(default=1, choices=TRANSACTION_STATUS)

    class Meta:
        db_table = "transaction"
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return str(self.transaction_id)
