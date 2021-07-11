from user.models import TgUser
from .utils.exception import PaycomException
from .utils.format import BaseFormat

from ..models import BalanceTransaction


class UserController:
    STATE_AVAILABLE = 0
    STATE_WAITING_PAY = 1
    STATE_PAY_ACCEPTED = 2
    STATE_CANCELLED = 3
    STATE_DELIVERED = 4

    response_message = None

    def __init__(self, request_id):
        self.request_id = request_id

    def validate(self, account_params):
        account = account_params['account']
        id = 'user_id'
        amount_str = 'amount'

        if id not in account or account[id] == '':
            self.response_message = {
                "code": PaycomException.ERROR_INVALID_ACCOUNT,
                "message": {
                    "ru": "Стир(ИНН)  пустой",
                    "uz": "Стир(ИНН)  kiritilmadi",
                    "en": "Stir(INN)  is empty"
                },
                "data": id
            }
            return False
        elif amount_str not in account_params or account_params[amount_str] == '' or \
                BaseFormat.is_not_numeric(value=account_params[amount_str]):
            self.response_message = {
                "code": PaycomException.ERROR_INVALID_AMOUNT,
                "message": {
                    "ru": "Сумма не существует.",
                    "uz": "Narxi mavjud emas.",
                    "en": "Amount does not exist."
                },
                "data": amount_str
            }
            return False
        else:
            try:
                id = int(account[id])
                user = TgUser.objects.get(tg_id=id)
                data = {
                    "Phone number": str(user.tel),
                    "Username": str(user.name),
                    "To'lov turi": "Hisob to'ldirish uchun",
                    "Balance": str(user.balance),
                }
                if user.status == 3:
                    self.response_message = {
                        "code": PaycomException.ERROR_INVALID_ACCOUNT,
                        "message": {
                            "ru": "Пользователь отключен или неактивен",
                            "uz": "Foydalanuvchi o'chirilgan yoki faol emas",
                            "en": "User is disabled or inactive"
                        },
                        "data": id
                    }
                    return False
                else:
                    self.response_message = {'allow': True, "additional": data}
                    return True
            except TgUser.DoesNotExist:
                self.response_message = {
                    "code": PaycomException.ERROR_INVALID_ACCOUNT,
                    "message": {
                        "ru": "Пользователь не найден",
                        "uz": "Foydalanuvchi topilmadi",
                        "en": "User not found"
                    },
                    "data": id
                }
                return False
