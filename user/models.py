from django.db import models
from django.utils import timezone

USER_STATUS = ((1, 'Active'), (2, 'Blocked'), (3, 'Deleted'))


class TgUser(models.Model):
    tg_id = models.IntegerField(verbose_name='Foydalanuvchi ID')
    name = models.CharField(max_length=150, verbose_name='Foydalanuvchi ismi', null=True,
                            blank=True)
    username = models.CharField(max_length=25, null=True, blank=True)
    tel = models.CharField(max_length=25, null=True, blank=True, verbose_name='Telefon raqam')
    status = models.IntegerField(choices=USER_STATUS, default=1)
    CHOICES = (
        ('oz', 'O\'zbek'),
        ('uz', 'Узбек'),
        ('ru', 'Руский'),
        ('en', 'Ingliz'),
    )
    lan = models.CharField(choices=CHOICES, max_length=2, verbose_name='Foydalanuvchi tili',
                           null=True, blank=True)

    block_count = models.IntegerField(default=0, verbose_name='Bloklanishlar soni')
    step = models.IntegerField(default=0, verbose_name='TEGILMASIN!!!')
    balance = models.IntegerField(default=0, verbose_name='Foydalanuvchi hisobi')
    # balance = models.DecimalField(max_digits=18, decimal_places=2, default=0) pul bilan
    # ishlaganda DecimalField ishlatgan yaxshi
    create_at = models.DateTimeField(default=timezone.now, verbose_name='Qo\'shilgan vaqti')

    class Meta:
        verbose_name = "Foydalanuvchilar"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return self.name
