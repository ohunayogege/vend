from django.urls import re_path as url
from .views import Airtime, BillsPayment, CablePayment, DataPlans, Transactions, ValidateIUCMeter


urlpatterns = [
    url(r'fetch-data\/?$', DataPlans.as_view()),
    url(r'fetch-data/(?P<network>[\w-]+)\/?$', DataPlans.as_view()),
    url(r'data\/?$', DataPlans.as_view()),
    url(r'topup\/?$', Airtime.as_view()),
    url(r'billpayment\/?$', BillsPayment.as_view()),
    url(r'cablesub/(?P<decoder>[\w-]+)\/?$', CablePayment.as_view()),
    url(r'cablesub\/?$', CablePayment.as_view()),

    url(r'validate/(?P<val>[\w-]+)\/?$', ValidateIUCMeter.as_view()),

    url(r'transactions\/?$', Transactions.as_view()),
    url(r'transactions/(?P<ref>[\w-]+)\/?\/?$', Transactions.as_view()),
]