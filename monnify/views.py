from django.http import JsonResponse
from django.shortcuts import render
import json
# Create your views here.

# @csrf_exempt
def Webhook(request):
    params = request.body
    r = json.loads(params)
    print(r)
    msg = {"success"}
    return JsonResponse(msg)