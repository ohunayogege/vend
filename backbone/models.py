from django.db import models
from django.utils.translation import gettext_lazy as _



class WebsiteConfig(models.Model):
    website_name = models.CharField(_("Website Name"), max_length=100, default="")
    website_title = models.CharField(_("Website Title"), max_length=100, default="")
    website_email = models.CharField(_("Website Email"), max_length=100, default="")
    whatsapp_number = models.CharField(_("WhatsApp Number"), max_length=100, default="")
    website_logo = models.FileField(upload_to="logo", blank=True)
    website_icon = models.FileField(upload_to="icon", blank=True)
    about_website = models.TextField(_("About Website"), default="", blank=True)
    website_location = models.TextField(_("Location"), default="", blank=True)
    prefix = models.CharField(_("Prefix"), max_length=20, default="PC", blank=True)
    bank_name = models.CharField(_("Bank Name"), max_length=100, default="", blank=True)
    account_name = models.CharField(_("Account Name"), max_length=100, default="", blank=True)
    account_number = models.CharField(_("Account Number"), max_length=100, default="", blank=True)
    facebook_link = models.CharField(_("Facebook URL"), max_length=100, default="#", blank=True)
    instagram_link = models.CharField(_("Instagram URL"), max_length=100, default="#",blank=True)
    whatsapp_link = models.CharField(_("WhatsApp URL"), max_length=100, default="#", blank=True)
    twitter_link = models.CharField(_("Twitter URL"), max_length=100, default="#", blank=True)
    transfer_charges = models.DecimalField(_("Transfer Charges"), max_digits=10, decimal_places=2, default=50.00)
    card_charges = models.DecimalField(_("Card Charges"), max_digits=10, decimal_places=2, default=0.00)
    min_bonus_transfer = models.DecimalField(_("Minimum Bonus Transfer"), max_digits=10, decimal_places=2, default=0.00)
    reseller_price = models.DecimalField(_("Reseller Price"), max_digits=10, decimal_places=2, default=0.00)
    whatsapp_group_link = models.CharField(_("Whatsapp Group Link"), max_length=60, default='')

    # SEO
    seo_description = models.TextField(default='', blank=True)
    seo_keywords = models.TextField(default='', blank=True)

    def __str__(self):
        return self.website_name

class APISetting(models.Model):
    monnify_secret_key = models.CharField(_("Monnify Secret Key"), max_length=100, default="")
    monnify_api_key = models.CharField(_("Monnify API Key"), max_length=100, default="")
    monnify_contract_code = models.CharField(_("Monnify Contract Code"), max_length=100, default="")
    vtu_key = models.CharField(_("VTU API Token"), max_length=100, default="")

    def __str__(self):
        return "API Settings"


class AirtimeToCashCalc(models.Model):
    glo = models.DecimalField(_("GLO Percentage %"), decimal_places=2, max_digits=10, default=80)
    glo_number = models.CharField(_("GLO Number"), max_length=20, default='')
    mtn = models.DecimalField(_("MTN Percentage %"), decimal_places=2, max_digits=10, default=85)
    mtn_number = models.CharField(_("MTN Number"), max_length=20, default='')
    airtel = models.DecimalField(_("Airtel Percentage %"), decimal_places=2, max_digits=10, default=75)
    airtel_number = models.CharField(_("Airtel Number"), max_length=20, default='')
    etisalat = models.DecimalField(_("9mobile Percentage %"), decimal_places=2, max_digits=10, default=65)
    etisalat_number = models.CharField(_("9mobile Number"), max_length=20, default='')
    notification_number = models.CharField(_("Notification Number"), max_length=20, default='08149983395')

    def __str__(self):
        return "Airtime To Cash Percentage"


class AirtimeRequest(models.Model):
    user = models.ForeignKey("web.User", on_delete=models.CASCADE, default=None)
    amount = models.DecimalField(_("Amount"), decimal_places=2, max_digits=10, default=0)
    cash_back = models.DecimalField(_("Cash Back"), decimal_places=2, max_digits=10, default=0)
    method = models.CharField(max_length=60, default='')
    mobile = models.CharField(max_length=40, default='')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class DataCommission(models.Model):
    mtn = models.DecimalField(_("MTN Customer Percentage"), max_digits=10, decimal_places=2, default=0.0)
    # mtn_api = models.DecimalField(_("MTN API Percentage"), max_digits=10, decimal_places=2, default=0.0)
    mtn_res = models.DecimalField(_("MTN Reseller Percentage"), max_digits=10, decimal_places=2, default=0.0)
    glo = models.DecimalField(_("Glo Customer Percentage"), max_digits=10, decimal_places=2, default=0.0)
    # glo_api = models.DecimalField(_("Glo API Percentage"), max_digits=10, decimal_places=2, default=0.0)
    glo_res = models.DecimalField(_("Glo Reseller Percentage"), max_digits=10, decimal_places=2, default=0.0)
    airtel = models.DecimalField(_("Airtel Customer Percentage"), max_digits=10, decimal_places=2, default=0.0)
    # airtel_api = models.DecimalField(_("Airtel API Percentage"), max_digits=10, decimal_places=2, default=0.0)
    airtel_res = models.DecimalField(_("Airtel Reseller Percentage"), max_digits=10, decimal_places=2, default=0.0)
    etisalat = models.DecimalField(_("9mobile Customer Percentage"), max_digits=10, decimal_places=2, default=0.0)
    # etisalat_api = models.DecimalField(_("9mobile API Percentage"), max_digits=10, decimal_places=2, default=0.0)
    etisalat_res = models.DecimalField(_("9mobile Reseller Percentage"), max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return "Data Commission"


class DataSetting(models.Model):
    mtn_sme_is_active = models.BooleanField(default=True)
    mtn_gifting_is_active = models.BooleanField(default=True)
    mtn_cg_is_active = models.BooleanField(default=True)
    airtel_gifting_is_active = models.BooleanField(default=True)
    airtel_cg_is_active = models.BooleanField(default=True)
    glo_gifting_is_active = models.BooleanField(default=True)
    etisalat_gifting_is_active = models.BooleanField(default=True)
    dstv_is_active = models.BooleanField(default=True)
    gotv_is_active = models.BooleanField(default=True)
    startimes_is_active = models.BooleanField(default=True)
    disco_is_active = models.BooleanField(default=True)

    def __str__(self):
        return "Data Settings"


class AirtimeCommission(models.Model):
    mtn = models.DecimalField(_("MTN Customer Percentage"), max_digits=10, decimal_places=2, default=0.0)
    # mtn_api = models.DecimalField(_("MTN API Percentage"), max_digits=10, decimal_places=2, default=0.0)
    mtn_res = models.DecimalField(_("MTN Reseller Percentage"), max_digits=10, decimal_places=2, default=0.0)
    glo = models.DecimalField(_("Glo Customer Percentage"), max_digits=10, decimal_places=2, default=0.0)
    # glo_api = models.DecimalField(_("Glo API Percentage"), max_digits=10, decimal_places=2, default=0.0)
    glo_res = models.DecimalField(_("Glo Reseller Percentage"), max_digits=10, decimal_places=2, default=0.0)
    airtel = models.DecimalField(_("Airtel Customer Percentage"), max_digits=10, decimal_places=2, default=0.0)
    # airtel_api = models.DecimalField(_("Airtel API Percentage"), max_digits=10, decimal_places=2, default=0.0)
    airtel_res = models.DecimalField(_("Airtel Reseller Percentage"), max_digits=10, decimal_places=2, default=0.0)
    etisalat = models.DecimalField(_("9mobile Customer Percentage"), max_digits=10, decimal_places=2, default=0.0)
    # etisalat_api = models.DecimalField(_("9mobile API Percentage"), max_digits=10, decimal_places=2, default=0.0)
    etisalat_res = models.DecimalField(_("9mobile Reseller Percentage"), max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return "Airtime Commission"

class BillsCommission(models.Model):
    decoder = models.DecimalField(_("Decoder Customer Percentage"), max_digits=10, decimal_places=2, default=0.0)
    # decoder_api = models.DecimalField(_("Decoder API Percentage"), max_digits=10, decimal_places=2, default=0.0)
    decoder_res = models.DecimalField(_("Decoder Reseller Percentage"), max_digits=10, decimal_places=2, default=0.0)
    decoder_ven = models.DecimalField(_("Decoder Vendor Percentage"), max_digits=10, decimal_places=2, default=0.0)
    edc = models.DecimalField(_("EDC Customer Percentage"), max_digits=10, decimal_places=2, default=0.0)
    # edc_api = models.DecimalField(_("EDC API Percentage"), max_digits=10, decimal_places=2, default=0.0)
    edc_res = models.DecimalField(_("EDC Reseller Percentage"), max_digits=10, decimal_places=2, default=0.0)
    edc_ven = models.DecimalField(_("EDC Vendor Percentage"), max_digits=10, decimal_places=2, default=0.0)
    smile = models.DecimalField(_("Smile Customer Percentage"), max_digits=10, decimal_places=2, default=0.0)
    # smile_api = models.DecimalField(_("Smile API Percentage"), max_digits=10, decimal_places=2, default=0.0)
    smile_res = models.DecimalField(_("Smile Reseller Percentage"), max_digits=10, decimal_places=2, default=0.0)
    smile_ven = models.DecimalField(_("Smile Vendor Percentage"), max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return "Data Commission"

class RechargeCard(models.Model):
    reference = models.CharField(max_length=60, default='')
    network = models.CharField(max_length=30, default='')
    denomination = models.CharField(max_length=30, default='')
    pin = models.CharField(max_length=100, default='')
    status = models.CharField(max_length=20, default='Unused')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "E-Cards"


class EPin(models.Model):
    reference = models.CharField(max_length=60, default='')
    exams = models.CharField(max_length=60, default='')
    pin = models.CharField(max_length=60, default='')
    status = models.CharField(max_length=20, default='Unused')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "E-Pins"

class ECardSettings(models.Model):
    waec_price_users = models.DecimalField(_("WAEC User Price"), max_digits=10, decimal_places=2, default=0.0)
    waec_price_res = models.DecimalField(_("WAEC Reseller Price"), max_digits=10, decimal_places=2, default=0.0)
    # waec_price_api = models.DecimalField(_("WAEC API Price"), max_digits=10, decimal_places=2, default=0.0)
    neco_price_users = models.DecimalField(_("NECO User Price"), max_digits=10, decimal_places=2, default=0.0)
    neco_price_res = models.DecimalField(_("NECO Reseller Price"), max_digits=10, decimal_places=2, default=0.0)
    # neco_price_api = models.DecimalField(_("NECO API Price"), max_digits=10, decimal_places=2, default=0.0)

    mtn_discount_users = models.DecimalField(_("MTN User Discounts"), max_digits=10, decimal_places=2, default=0.0)
    mtn_discount_res = models.DecimalField(_("MTN Reseller Discounts"), max_digits=10, decimal_places=2, default=0.0)
    # mtn_discount_api = models.DecimalField(_("MTN API Discounts"), max_digits=10, decimal_places=2, default=0.0)
    airtel_discount_users = models.DecimalField(_("Airtel User Discounts"), max_digits=10, decimal_places=2, default=0.0)
    airtel_discount_res = models.DecimalField(_("Airtel Reseller Discounts"), max_digits=10, decimal_places=2, default=0.0)
    # airtel_discount_api = models.DecimalField(_("Airtel API Discounts"), max_digits=10, decimal_places=2, default=0.0)
    glo_discount_users = models.DecimalField(_("GLO User Discounts"), max_digits=10, decimal_places=2, default=0.0)
    glo_discount_res = models.DecimalField(_("GLO Reseller Discounts"), max_digits=10, decimal_places=2, default=0.0)
    # glo_discount_api = models.DecimalField(_("GLO API Discounts"), max_digits=10, decimal_places=2, default=0.0)
    etisalat_discount_users = models.DecimalField(_("9mobile User Discounts"), max_digits=10, decimal_places=2, default=0.0)
    etisalat_discount_res = models.DecimalField(_("9mobile Reseller Discounts"), max_digits=10, decimal_places=2, default=0.0)
    # etisalat_discount_api = models.DecimalField(_("9mobile API Discounts"), max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return "Recharge Pin Settings"

class ReferralSystem(models.Model):
    referral_bonus = models.DecimalField(_("Referral Percentage"), max_digits=10, decimal_places=2, default=0.0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Referral System"

class ContactList(models.Model):
    name = models.CharField(_("Name"), max_length=60, default='')
    whatsapp_link = models.CharField(_("Whatsapp Link"), max_length=60, default='')

    def __str__(self):
        return f"{self.name} - {self.whatsapp_link}"


class Announcement(models.Model):
    title = models.CharField(max_length=100, default='')
    message = models.TextField(default='')
    popup = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

