import os
from base64 import standard_b64decode

from ..models import PaymentMethods

# MERCHANT = '6030eac1a10b214d8d11d5ac'
# PROD_KEY = 'mz83DdSgfM1@DG&Q3Tabxcp2omWBp&9O&wOr'
# TEST_KEY = 'nJFUzTTNxuv?NgMxIIvAygFjTVCpkMivp6Oy'
# O'rmon texnoservis transit schet
MERCHANT = '6034a109a10b214d8d120d34'
PROD_KEY = '@3%tSV#CXyyKktKQgW96S@st#EXb#MCDW?K1'
TEST_KEY = 'amD&DBEFG25#gSuJzUapx5u99#GGgodkR3pj'


class MerchantAPI:
    header = None
    auth_data = None

    def __init__(self, request):
        self.header = request.META.get('HTTP_AUTHORIZATION', None)
        self.auth_data = self.header.split()[1] if self.header is not None else ''

    def authorize(self):
        if 'PAYCOM_PROTOCOL_APP_TESTKEY' not in os.environ:
            os.environ['PAYCOM_PROTOCOL_APP_TESTKEY'] = TEST_KEY
        key = os.environ['PAYCOM_PROTOCOL_APP_TESTKEY']
        merchant_auth = f'Paycom:{key}'
        paycom_auth = standard_b64decode(self.auth_data).decode("utf-8")
        if merchant_auth != paycom_auth or self.header is None:
            return False
        return True
