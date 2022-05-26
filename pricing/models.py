from django.db import models

from utils.constant import NETWORK_TYPE


class MTNData(models.Model):
    plan_size = models.CharField(max_length=100, default='')
    customer_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    reseller_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    api_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    validity = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"MTN Data - {self.plan_size}"


class GLOData(models.Model):
    plan_size = models.CharField(max_length=100, default='')
    customer_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    reseller_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    api_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    validity = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"GLO Data - {self.plan_size}"

class AirtelData(models.Model):
    plan_size = models.CharField(max_length=100, default='')
    customer_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    reseller_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    api_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    validity = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"Airtel Data - {self.plan_size}"

class EtisalatData(models.Model):
    plan_size = models.CharField(max_length=100, default='')
    customer_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    reseller_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    api_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    validity = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"9mobile Data - {self.plan_size}"

class EPin(models.Model):
    network_type = models.CharField(max_length=100, default='', choices=NETWORK_TYPE)
    default_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    customer_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    reseller_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    api_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.network_type}"


class General(models.Model):
    service_type = models.CharField(max_length=100, default='')
    customer_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    reseller_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    api_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.service_type}"


