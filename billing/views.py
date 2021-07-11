import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .utils.paycom.api import PaycomAPI
from django.views import View
from django.http import JsonResponse


@method_decorator(csrf_exempt, name='dispatch')
class PaycomView(View):
    """http://127.0.0.1:8000/paycom/api"""

    def post(self, request):
        app = PaycomAPI(request=request)
        response = app.run()
        new_data = json.loads(response)
        return JsonResponse(data=new_data, safe=False)

    def get(self, request):
        return JsonResponse(data={"message": " Bu url faqat post request qabul qiladi "})
