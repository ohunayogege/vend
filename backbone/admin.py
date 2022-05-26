from django.contrib import admin
from .models import AirtimeCommission, AirtimeRequest, AirtimeToCashCalc, APISetting, BillsCommission, ContactList,\
    DataCommission, DataSetting, ECardSettings, EPin, RechargeCard, ReferralSystem, WebsiteConfig


# admin.site.register(WebsiteConfig)
@admin.register(WebsiteConfig)
class WebsiteConfigAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): # Here
        return not WebsiteConfig.objects.exists()

@admin.register(APISetting)
class APISettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): # Here
        return not APISetting.objects.exists()

@admin.register(AirtimeToCashCalc)
class AirtimeToCashCalcAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): # Here
        return not AirtimeToCashCalc.objects.exists()


@admin.register(DataCommission)
class DataCommissionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): # Here
        return not DataCommission.objects.exists()

@admin.register(AirtimeCommission)
class AirtimeCommissionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): # Here
        return not AirtimeCommission.objects.exists()

@admin.register(BillsCommission)
class BillsCommissionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): # Here
        return not BillsCommission.objects.exists()

@admin.register(ReferralSystem)
class ReferralSystemAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): # Here
        return not ReferralSystem.objects.exists()

@admin.register(ContactList)
class ContactListAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): # Here
        return not ContactList.objects.exists()

@admin.register(ECardSettings)
class ECardSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): # Here
        return not ECardSettings.objects.exists()

@admin.register(DataSetting)
class DataSettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): # Here
        return not DataSetting.objects.exists()

admin.site.register(RechargeCard)
admin.site.register(EPin)
admin.site.register(AirtimeRequest)
