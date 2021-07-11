from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path('api', views.PaycomView.as_view(), name="paycom"),
]