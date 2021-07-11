import os
from base64 import standard_b64decode


MERCHANT = ''
PROD_KEY = ''
TEST_KEY = ''


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
