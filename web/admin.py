from django.contrib import admin
from .models import User, UserBank, UserNotification, UserRef, UserVerify, Wallet

admin.site.register(User)
admin.site.register(UserBank)
admin.site.register(UserNotification)
admin.site.register(UserRef)
admin.site.register(UserVerify)
admin.site.register(Wallet)
