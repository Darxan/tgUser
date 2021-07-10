import json
from datetime import datetime

from django.utils import timezone

from .utils.format import BaseFormat
from .utils.pstatus import PaycomStatus
from ..models import BalanceTransaction, User


class Transactions(PaycomStatus):
    params = None
    paycom_transaction_id = None
    transaction = None
    order = None
    formatter = BaseFormat()

    def __init__(self, params):
        self.params = params
        self.paycom_transaction_id = params['id'] if 'id' in params else 0

    def exist(self):
        try:
            self.transaction = BalanceTransaction.objects.get(transaction_id=self.paycom_transaction_id)
            return True
        except BalanceTransaction.DoesNotExist:
            return False

    def save_transaction(self):
        # order = OrderModel.objects.get(order_id=self.params['account']['id'])
        # order.state = UserController.STATE_WAITING_PAY
        # order.save()
        """
            Bizda order mavjud bolmaganligi uchun order statusi update qilinmayapti
            Comment:
            Save transaction with state = 1 and set order state STATE_WAITING_PAY = 1
            self.transaction = new transaction
        """
        data = {
            'user': User.objects.get(stir=self.params['account']['id']),  # inn
            'transaction_id': self.paycom_transaction_id,
            'time_millisecond': self.params['time'],
            'amount': self.params['amount'] / 100,
            'state': self.STATE_CREATED,
            'type': 1,  # kirim
        }
        self.transaction = BalanceTransaction.objects.create(**data)

    def check_transaction_state(self, state=None):
        if state is None:
            state = self.STATE_CREATED
        return True if self.transaction.state == state else False

    def transaction_is_expired(self):
        time_interval = (timezone.now() - self.transaction.created_at)
        if self.formatter.datetime_timedelta_to_milliseconds(_datetime=time_interval) > self.TIMEOUT:
            return True
        else:
            return False

    def return_transaction_details(self, field=None):

        """
            Comment: state, create_time|perform_time, transaction, receivers
        """
        if field is None:
            field = 'created_at'
        _datetime = getattr(self.transaction, field)
        time_in_milliseconds = self.formatter.millisecond_timestamp_from_utc_to_time_zone(utc_datetime=_datetime)
        response = {
            'result': {
                'state': self.transaction.state,
                'transaction': str(self.transaction.id)
            }
        }
        if field == 'created_at':
            response['result']['create_time'] = time_in_milliseconds
        else:
            response['result'][field] = time_in_milliseconds
        return json.dumps(response)

    def cancel_transaction(self, reason, state=None):
        print("reason", reason)
        print("state", state)
        if state is None:
            state = self.STATE_CANCELLED
        self.transaction.state = state

        self.transaction.cancel_time = timezone.now()
        self.transaction.reason = reason
        self.transaction.save()

    def complete_transaction(self):
        self.transaction.state = self.STATE_COMPLETED
        self.transaction.perform_time = timezone.now()
        self.transaction.save()

    def get_transaction_details(self):
        cancel_time = self.formatter.millisecond_timestamp_from_utc_to_time_zone(utc_datetime=self.transaction.cancel_time)
        perform_time = self.formatter.millisecond_timestamp_from_utc_to_time_zone(utc_datetime=self.transaction.perform_time)
        create_time = self.formatter.millisecond_timestamp_from_utc_to_time_zone(utc_datetime=self.transaction.created_at)
        reason = int(self.transaction.reason) if self.transaction.reason is not None else None
        data = {
            "result": {
                "create_time": create_time,
                "perform_time": perform_time,
                "cancel_time": cancel_time,
                "transaction": str(self.transaction.id),
                "state": self.transaction.state,
                "reason": reason
            }
        }
        return json.dumps(data)

    def get_statement(self, _from, _to):
        datetime_from = datetime.utcfromtimestamp(_from / 1000.0)
        datetime_to = datetime.utcfromtimestamp(_to / 1000.0)
        timezone_from = timezone.make_aware(datetime_from, timezone.get_current_timezone())
        timezone_to = timezone.make_aware(datetime_to, timezone.get_current_timezone())
        transactions = BalanceTransaction.objects.filter(
            created_at__range=[timezone_from, timezone_to], reason__isnull=True
        )

        regenerated_transactions = [{
            "id": item.transaction_id,
            "time": item.created_at,
            "amount": item.amount,
            "account": {
                "id": item.user.id
            },
            "create_time": self.formatter.millisecond_timestamp_from_utc_to_time_zone(item.created_at),
            "perform_time": self.formatter.millisecond_timestamp_from_utc_to_time_zone(item.perform_time),
            "cancel_time": 0,
            "transaction": item.id,
            "state": 2,
            "reason": None,
            "receivers": []
        } for item in transactions]
        data = {
            "result": {
                "transactions": regenerated_transactions
            }
        }
        return json.dumps(data)
