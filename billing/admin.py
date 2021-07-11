from django.contrib import admin

from billing.models import BalanceTransaction


class BalanceTransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "transaction_id", "time_millisecond", "time_datetime", "perform_time",
                    "create_time", "cancel_time", "error", "type", "amount", "reason", "state",
                    "balance_updated",
                    )


admin.site.register(BalanceTransaction, BalanceTransactionAdmin)
