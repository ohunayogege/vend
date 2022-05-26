from django.urls import re_path as url
from .views import Webhook

urlpatterns = [
    url(r'^webhook/', Webhook),
]
