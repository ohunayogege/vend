from django.db import models
from datetime import timedelta
from datetime import datetime as dt
from django.dispatch import receiver
from utils.functions import gen_ref_id
from utils.managers import UserManager
from django.utils.text import slugify
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from utils.constant import STAFF_ROLE, USER_TYPE


class User(AbstractUser):
	username = models.CharField(_('Username'), max_length=60, default="", unique=True)
	first_name = models.CharField(_('First Name'), max_length=100, default="")
	last_name = models.CharField(_('Last Name'), max_length=100, default="")
	email = models.EmailField(_('email address'), default="")
	mobile = models.CharField(max_length = 20, default='')
	address = models.CharField(max_length = 100, default='', blank=True)
	user_type = models.CharField(max_length=20, default='customer', choices=USER_TYPE)
	transaction_pin = models.CharField(max_length=4, default='', blank=True)
	# Payout Bank
	bank_name = models.CharField(max_length=30, default='', blank=True)
	account_name = models.CharField(max_length=60, default='', blank=True)
	account_number = models.CharField(max_length=11, default='', blank=True)
	bank_set = models.BooleanField(default=False)
	staff_type = models.CharField(max_length=20, default='None', choices=STAFF_ROLE)
	
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

	objects = UserManager()
	
	def __str__(self):
		return f"{self.first_name} {self.last_name} - {self.mobile}"
	
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)


class UserRef(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
	code = models.CharField(max_length=8, default="", blank=True)
	referred_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, related_name="referred_by")
	first_bonus = models.BooleanField(default=False)
	modified = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username

	def get_referred(self):
		pass

	def save(self, *args, **kwargs):
		if self.code == "":
			code = gen_ref_id(8)
			check_code = UserRef.objects.filter(code=code).exists()
			while(check_code):
				code = gen_ref_id(8)
			else:
				self.code = self.user.username
		super().save(*args, **kwargs)


class Wallet(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
	amount = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
	bonus = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
	def __str__(self):
		return f"{self.user.first_name} {self.user.last_name} - ₦{self.amount}"


class UserBank(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	wallet_code = models.CharField(max_length=30, default='', blank=True)
	bank_name = models.CharField(max_length=30, default='', blank=True)
	bank_slug = models.SlugField(max_length=60, default='', blank=True)
	account_name = models.CharField(max_length=60, default='', blank=True)
	account_number = models.CharField(max_length=11, default='', blank=True)

	def __str__(self):
		return f"{self.user.first_name} {self.user.last_name} - {self.bank_name}"
	
	def save(self, *args, **kwargs):
		if not self.bank_slug:
			self.bank_slug = slugify(self.bank_name)
		super(UserBank, self).save(*args, **kwargs)


class UserVerify(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
	token = models.CharField(max_length=100, default='')
	expires_in = models.DateTimeField(auto_now_add=False)

	def __str__(self):
		return f"{self.token} - {self.user.email}"

class UserNotification(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	title = models.CharField(max_length=100, default='')
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username}"

class UserGenPin(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	exams = models.CharField(max_length=60, default='')
	pin = models.CharField(max_length=60, default='')
	reference = models.CharField(max_length=60, default='')
	status = models.CharField(max_length=20, default='Unused')
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.pin} - {self.exams}"

class UserGenCard(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	network = models.CharField(max_length=60, default='')
	denomination = models.CharField(max_length=60, default='')
	pin = models.CharField(max_length=60, default='')
	reference = models.CharField(max_length=60, default='')
	status = models.CharField(max_length=20, default='Unused')
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.pin} - {self.network} - {self.denomination}"
