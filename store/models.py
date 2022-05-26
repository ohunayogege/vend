from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class CableList(models.Model):
	decoder = models.CharField(max_length=60, default='')
	slug = models.SlugField(max_length=60, default='', blank=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.decoder
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.decoder)
		super(CableList, self).save(*args, **kwargs)

class CablePlan(models.Model):
	pid = models.CharField(max_length=25, default='')
	decoder = models.ForeignKey(CableList, on_delete=models.CASCADE, default=None)
	plan = models.CharField(max_length=100, default='')
	amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	customer_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	reseller_user_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	api_user_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	vendor_user_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	active = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.decoder} - {self.pid}: {self.plan}"


class NetworkList(models.Model):
	network = models.CharField(max_length=60, default='')
	slug = models.SlugField(max_length=60, default='', blank=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.network
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.network)
		super(NetworkList, self).save(*args, **kwargs)


class DataPlan(models.Model):
	pid = models.CharField(max_length=25, default='')
	network = models.ForeignKey(NetworkList, on_delete=models.CASCADE, default=None)
	plan = models.CharField(max_length=100, default='')
	plan_type = models.CharField(max_length=60, default='', blank=True)
	amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	customer_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	reseller_user_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	api_user_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	vendor_user_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	active = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.network} - {self.pid}: {self.plan}"


class Disco(models.Model):
	pid = models.CharField(max_length=25, default='')
	disco_name = models.CharField(max_length=60, default='')
	disco_slug = models.CharField(max_length=100, default='')
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.disco_name
	
	def save(self, *args, **kwargs):
		if not self.disco_slug:
			self.disco_slug = slugify(self.disco_name)
		super(Disco, self).save(*args, **kwargs)
