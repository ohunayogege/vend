from django.contrib import admin

from pricing.models import AirtelData, EPin, EtisalatData, GLOData, General, MTNData

# Register your models here.
admin.site.register(General)
admin.site.register(EPin)
admin.site.register(MTNData)
admin.site.register(GLOData)
admin.site.register(AirtelData)
admin.site.register(EtisalatData)
