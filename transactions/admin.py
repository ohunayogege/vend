from django.contrib import admin

from transactions.models import Transaction, WalletHistory

# Register your models here.
admin.site.register(WalletHistory)
admin.site.register(Transaction)