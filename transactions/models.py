from django.db import models
from utils.constant import TRANSACTION_STATUS


class Transaction(models.Model):
	user = models.ForeignKey("web.User", on_delete=models.CASCADE, default=None)
	reference = models.CharField(max_length=100, default='', blank=True)
	ps_ref = models.CharField(max_length=100, default='', blank=True)
	amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	amount_before = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	amount_after = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	method = models.CharField(max_length=100, default='', blank=True)
	trans_type = models.CharField(max_length=100, default='', blank=True)
	credit = models.BooleanField(default=False)
	status = models.CharField(max_length=30, default='pending', choices=TRANSACTION_STATUS, blank=True)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.email

class WalletHistory(models.Model):
	user = models.ForeignKey("web.User", on_delete=models.CASCADE, default=None)
	reference = models.CharField(max_length=100, default='', blank=True)
	ps_ref = models.CharField(max_length=100, default='', blank=True)
	amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	amount_before = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	amount_after = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	method = models.CharField(max_length=100, default='', blank=True)
	trans_type = models.CharField(max_length=100, default='', blank=True)
	credit = models.BooleanField(default=False)
	status = models.CharField(max_length=30, default='pending', blank=True)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.email