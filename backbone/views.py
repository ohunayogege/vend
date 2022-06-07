from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import redirect, render
from backbone.forms import EPinForm, StaffForm
from backbone.models import APISetting, AirtimeCommission, AirtimeRequest, AirtimeToCashCalc, Announcement, BillsCommission, ContactList, DataCommission, DataSetting, ECardSettings, EPin, RechargeCard, ReferralSystem, WebsiteConfig
from transactions.models import Transaction, WalletHistory
from utils.api import TVBills, fetchPlans, getUserDetail
from utils.functions import Banks, gen_key, gen_ref_id, is_ajax
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from web.models import User, Wallet
from store.models import CableList, CablePlan, DataPlan, NetworkList

def FetchDatas(request):
	return render(request, "back/datas.html")

def Home(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	income = 0
	expense = 0
	incs = Transaction.objects.filter(credit=True)
	exps = Transaction.objects.filter(credit=False, status='success')
	for inc in incs:
		income += inc.amount
	for exp in exps:
		expense += exp.amount
	users = User.objects.all().exclude(is_staff=True)
	det = getUserDetail()
	# print(det['data']['wallets'])
	ctx = {
		'users': len(users),
		'income': income,
		'expense': expense,
		'wallet_balance': det['data']['wallet_balance'],
		'banks': det['data']['banks'],
		"wallets": det['data']['wallets'],
	}
	return render(request, "back/home.html", ctx)

def Login(request):
	if request.user.is_authenticated:
		return redirect("a_home")
	if is_ajax(request=request):
		username = request.POST['username']
		password = request.POST['password']

		check_username = User.objects.filter(username=username).exists()
		if check_username == False:
			msg = {"status": False, "message": "Username is invalid"}
			return JsonResponse(msg)
		n_user = User.objects.get(username=username)
		if n_user.is_staff == False:
			msg = {"status": False, "message": "Invalid  Username/Password. Try again."}
			return JsonResponse(msg)
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			msg = {"status": True, "message": "Successfully logged in."}
			return JsonResponse(msg)
		else:
			msg = {"status": False, "message": "Invalid  Username/Password. Try again."}
			return JsonResponse(msg)
	return render(request, "back/login.html")


def Users(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	users = User.objects.filter(user_type='customer', is_staff=False).order_by("-pk")
	ctx = {
		'users': users
	}
	return render(request, "back/users.html", ctx)

def myProfile(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	
	if is_ajax(request=request):
		action = request.POST['action']
		user = request.user
		if action == 'profile':
			user.first_name = request.POST['first_name']
			user.last_name = request.POST['last_name']
			user.email = request.POST['email']
			user.mobile = request.POST['mobile']
			user.save()
			msg = {"status": True, "message": "Profile has been updated"}
			return JsonResponse(msg)
		elif action == 'password':
			new_password = request.POST['new_password']
			user.set_password(new_password)
			user.save()
			msg = {"status": True, "message": "Password has been updated"}
			return JsonResponse(msg)
	return render(request, "back/profile.html")

def DelUser(request, username):
	con = User.objects.get(username=username)
	con.delete()
	return redirect("a_users")

def Resellers(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	users = User.objects.filter(user_type='reseller', is_staff=False).order_by("-pk")
	ctx = {
		'users': users
	}
	return render(request, "back/resellers.html", ctx)


def APIUsers(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	users = User.objects.filter(user_type='api', is_staff=False).order_by("-pk")
	ctx = {
		'users': users
	}
	return render(request, "back/api_users.html", ctx)

def updateUserWallet(request, username):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	user = User.objects.get(username=username)
	wallet = Wallet.objects.get(user=user)
	website = WebsiteConfig.objects.last()
	ctx = {
		'u': user,
		'w': wallet
	}
	if is_ajax(request=request):
		service = request.POST['service']

		if service == 'add':
			amount = request.POST['amount']
			
			wallet.amount += Decimal(amount)
			wallet.save()
			WalletHistory.objects.create(
				user=user,
				reference = f"{website.prefix}-{gen_ref_id(14)}",
				ps_ref = f"{website.prefix}-{gen_ref_id(14)}",
				amount = Decimal(amount),
				fee = Decimal("0.00"),
				method = f"Manual Funding from {request.user.username.capitalize()} (Admin)",
				trans_type = f"Wallet Top-Up",
				credit = True,
				status = "success"
			)
			msg = {"status": True, "message": "Amount has been updated"}
			return JsonResponse(msg)
		elif service == 'deduct':
			amount = request.POST['amount']
			if wallet.amount < Decimal(amount):
				msg = {"status": False, "message": "User does not have sufficient balance."}
				return JsonResponse(msg)
			wallet.amount -= Decimal(amount)
			wallet.save()
			WalletHistory.objects.create(
				user=user,
				reference = f"{website.prefix}-{gen_ref_id(14)}",
				ps_ref = f"{website.prefix}-{gen_ref_id(14)}",
				amount = Decimal(amount),
				fee = Decimal("0.00"),
				method = f"Manual Debit from {request.user.username.capitalize()} (Admin)",
				trans_type = f"Wallet Top-Up",
				credit = True,
				status = "success"
			)
			msg = {"status": True, "message": "Amount has been updated"}
			return JsonResponse(msg)
	return render(request, 'back/wallet.html', ctx)


def UserProfile(request, username):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	user = User.objects.get(username=username)
	if is_ajax(request=request):
		action = request.POST['action']
		if action == 'profile':
			user.first_name = request.POST['first_name']
			user.last_name = request.POST['last_name']
			user.email = request.POST['email']
			user.mobile = request.POST['mobile']
			user.user_type = request.POST['user_type']
			user.bank_name = request.POST['bank_name']
			user.account_name = request.POST['account_name']
			user.account_number = request.POST['account_number']
			user.save()
			msg = {"status": True, "message": "Profile has been updated"}
			return JsonResponse(msg)
		elif action == 'password':
			new_password = request.POST['new_password']
			user.set_password(new_password)
			user.save()
			msg = {"status": True, "message": "Password has been updated"}
			return JsonResponse(msg)
	ctx = {
		"u": user
	}
	return render(request, "back/user.html", ctx)

def AdminUsers(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	users = User.objects.filter(is_staff=True).order_by("-pk")
	ctx = {
		'users': users
	}
	return render(request, "back/admin_users.html", ctx)


# Website Setup

def WebsiteDetails(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	website = WebsiteConfig.objects.last()
	ctx = {
		'website': website,
	}
	if is_ajax(request=request):
		website_name = request.POST['website_name']
		website_title = request.POST['website_title']
		website_email = request.POST['website_email']
		whatsapp_number = request.POST['whatsapp_number']
		about_website = request.POST['about_website']
		prefix = request.POST['prefix']
		business_location = request.POST['business_address']
		facebook_link = request.POST['facebook_link']
		twitter_link = request.POST['twitter_link']
		whatsapp_link = request.POST['whatsapp_link']
		instagram_link = request.POST['instagram_link']
		min_bonus_transfer = request.POST['min_bonus_transfer']
		card_charges = request.POST['card_charges']
		reseller_price = request.POST['reseller_price']
		transfer_charges = request.POST['transfer_charges']
		bank_name = request.POST['bank_name']
		account_name = request.POST['account_name']
		account_number = request.POST['account_number']
		whatsapp_group_link = request.POST['whatsapp_group_link']

		
		website.website_name = website_name
		website.website_title = website_title
		website.website_email = website_email
		website.whatsapp_number = whatsapp_number
		website.about_website = about_website
		website.prefix = prefix
		website.business_location = business_location
		website.facebook_link = facebook_link
		website.twitter_link = twitter_link
		website.whatsapp_link = whatsapp_link
		website.instagram_link = instagram_link
		website.min_bonus_transfer = min_bonus_transfer
		website.card_charges = card_charges
		website.reseller_price = reseller_price
		website.transfer_charges = transfer_charges
		website.bank_name = bank_name
		website.account_name = account_name
		website.account_number = account_number
		website.whatsapp_group_link = whatsapp_group_link
		website.save()
		msg = {"status": True, "message": "Settings Changed Successfully"}
		return JsonResponse(msg)
	return render(request, "back/website-settings.html", ctx)

def APISettings(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	api = APISetting.objects.last()
	ctx = {
		'api': api,
	}
	if is_ajax(request=request):
		monnify_secret = request.POST['monnify_key']
		monnify_api = request.POST['monnify_api']
		monnify_contract_code = request.POST['monnify_code']
		vtu_key = request.POST['vtu_key']

		api.vtu_key = vtu_key
		api.monnify_secret_key = monnify_secret
		api.monnify_api_key = monnify_api
		api.monnify_contract_code = monnify_contract_code
		api.save()
		msg = {"status": True, "message": "Settings Changed Successfully"}
		return JsonResponse(msg)
	return render(request, "back/api-settings.html", ctx)


def A2CSettings(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	a2c = AirtimeToCashCalc.objects.last()
	ctx = {
		'a2c': a2c,
	}
	if is_ajax(request=request):
		mtn_number = request.POST['mtn_number']
		airtel_number = request.POST['airtel_number']
		glo_number = request.POST['glo_number']
		etisalat_number = request.POST['etisalat_number']
		etisalat_percent = request.POST['etisalat_percent']
		mtn_percent = request.POST['mtn_percent']
		glo_percent = request.POST['glo_percent']
		airtel_percent = request.POST['airtel_percent']
		notification_number = request.POST['notification_number']
		
		a2c.mtn = mtn_percent
		a2c.mtn_number = mtn_number
		a2c.glo = glo_percent
		a2c.glo_number = glo_number
		a2c.airtel = airtel_percent
		a2c.airtel_number = airtel_number
		a2c.etisalat = etisalat_percent
		a2c.etisalat_number = etisalat_number
		a2c.notification_number = notification_number
		a2c.save()
		msg = {"status": True, "message": "Settings Changed Successfully"}
		return JsonResponse(msg)
	return render(request, "back/a2c-settings.html", ctx)

def LogoSettings(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	website = WebsiteConfig.objects.last()
	ctx = {
		'website': website
	}
	if request.method == "POST":
		upload_type = request.POST['upload_type']
		if upload_type == 'icon':
			icon = request.FILES['image-icon']
			website.website_icon = icon
			website.save()
			return redirect("a_home")
		else:
			logo = request.FILES['image-logo']
			website.website_logo = logo
			website.save()
			return redirect("a_home")
	return render(request, "back/website-logo.html", ctx)


def DataSettings(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	com = DataCommission.objects.last()
	ctx = {
		'com': com
	}
	if is_ajax(request=request):
		com.mtn = request.POST['mtn']
		com.mtn_api = request.POST['mtn_api']
		com.mtn_res = request.POST['mtn_res']
		com.glo = request.POST['glo']
		com.glo_res = request.POST['glo_res']
		com.glo_api = request.POST['glo_api']
		com.airtel = request.POST['airtel']
		com.airtel_res = request.POST['airtel_res']
		com.airtel_api = request.POST['airtel_api']
		com.etisalat = request.POST['etisalat']
		com.etisalat_api = request.POST['etisalat_api']
		com.etisalat_res = request.POST['etisalat_res']

		com.save()
		msg = {"status": True, "message": "Saved Successfully."}
		return JsonResponse(msg)
	return render(request, "back/data.html", ctx)

def AirtimeSettings(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	com = AirtimeCommission.objects.last()
	ctx = {
		'com': com
	}
	if is_ajax(request=request):
		com.mtn = request.POST['mtn']
		com.mtn_api = request.POST['mtn_api']
		com.mtn_res = request.POST['mtn_res']
		com.glo = request.POST['glo']
		com.glo_res = request.POST['glo_res']
		com.glo_api = request.POST['glo_api']
		com.airtel = request.POST['airtel']
		com.airtel_res = request.POST['airtel_res']
		com.airtel_api = request.POST['airtel_api']
		com.etisalat = request.POST['etisalat']
		com.etisalat_api = request.POST['etisalat_api']
		com.etisalat_res = request.POST['etisalat_res']

		com.save()
		msg = {"status": True, "message": "Saved Successfully."}
		return JsonResponse(msg)
	return render(request, "back/airtime.html", ctx)

def BillsSettings(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	com = BillsCommission.objects.last()
	ctx = {
		'com': com
	}
	if is_ajax(request=request):
		com.edc = request.POST['edc']
		com.edc_res = request.POST['edc_res']
		com.edc_api = request.POST['edc_api']
		# com.smile = request.POST['smile']
		# com.smile_res = request.POST['smile_res']
		# com.smile_api = request.POST['smile_api']
		# com.smile_ven = request.POST['smile_ven']

		com.save()
		msg = {"status": True, "message": "Saved Successfully."}
		return JsonResponse(msg)
	return render(request, "back/bills.html", ctx)

def ReferralSettings(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	ref = ReferralSystem.objects.last()
	ctx = {
		'ref': ref
	}
	if is_ajax(request=request):
		referral_bonus = request.POST['referral_bonus']
		status = request.POST['status']

		ref.referral_bonus = referral_bonus
		ref.status = status
		ref.save()
		msg = {"status": True, "message": "Referral Settings Changed Successfully."}
		return JsonResponse(msg)
	return render(request, "back/referral.html", ctx)


def SEOSettings(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	website = WebsiteConfig.objects.last()
	ctx = {
		'website': website
	}
	if is_ajax(request=request):
		keywords = request.POST['keywords']
		description = request.POST['description']

		website.seo_description = description
		website.seo_keywords = keywords
		website.save()

		msg = {"status": True, "message": "SEO Settings Updated Successfully."}
		return JsonResponse(msg)
	return render(request, "back/seo.html", ctx)


def Contacts(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	contacts = ContactList.objects.all()
	ctx = {
		'contacts': contacts
	}
	return render(request, "back/contacts.html", ctx)


def AddContact(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	if request.method == "POST":
		ContactList.objects.create(
			name=request.POST['name'],
			whatsapp_link=request.POST['whatsapp_link']
		)
		return redirect("a_contacts")
	return render(request, "back/contact.html")

def DelContact(request, pk):
	con = ContactList.objects.get(pk=pk)
	con.delete()
	return redirect("a_contacts")

def AllECards(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	pins = RechargeCard.objects.all().filter(network="MTN")
	ctx = {
		"pins": pins
	}
	if is_ajax(request=request):
		card_type = request.GET['card_type']
		if card_type == 'e_cards':
			RechargeCard.objects.filter(status="Used").delete()
			msg = {"status": True, "message": "Successfully deleted."}
			return JsonResponse(msg)
		else:
			EPin.objects.filter(status="Used").delete()
			msg = {"status": True, "message": "Successfully deleted."}
			return JsonResponse(msg)
	return render(request, 'back/e_card.html', ctx)

def AllECardsGlo(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	pins = RechargeCard.objects.all().filter(network="GLO")
	ctx = {
		"pins": pins
	}
	if is_ajax(request=request):
		card_type = request.GET['card_type']
		if card_type == 'e_cards':
			RechargeCard.objects.filter(status="Used").delete()
			msg = {"status": True, "message": "Successfully deleted."}
			return JsonResponse(msg)
		else:
			EPin.objects.filter(status="Used").delete()
			msg = {"status": True, "message": "Successfully deleted."}
			return JsonResponse(msg)
	return render(request, 'back/e_card_glo.html', ctx)

def AllECardsAirtel(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	pins = RechargeCard.objects.all().filter(network="Airtel")
	ctx = {
		"pins": pins
	}
	if is_ajax(request=request):
		card_type = request.GET['card_type']
		if card_type == 'e_cards':
			RechargeCard.objects.filter(status="Used").delete()
			msg = {"status": True, "message": "Successfully deleted."}
			return JsonResponse(msg)
		else:
			EPin.objects.filter(status="Used").delete()
			msg = {"status": True, "message": "Successfully deleted."}
			return JsonResponse(msg)
	return render(request, 'back/e_card_airtel.html', ctx)

def AllECards9mobile(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	pins = RechargeCard.objects.all().filter(network="9mobile")
	ctx = {
		"pins": pins
	}
	if is_ajax(request=request):
		card_type = request.GET['card_type']
		if card_type == 'e_cards':
			RechargeCard.objects.filter(status="Used").delete()
			msg = {"status": True, "message": "Successfully deleted."}
			return JsonResponse(msg)
		else:
			EPin.objects.filter(status="Used").delete()
			msg = {"status": True, "message": "Successfully deleted."}
			return JsonResponse(msg)
	return render(request, 'back/e_card_eti.html', ctx)

def ECards(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	website = WebsiteConfig.objects.last()
	if is_ajax(request=request):
		network = request.POST['network']
		denomination = request.POST['denomination']
		pins = request.POST['pins']
		e_pins = pins.split(",")
		for pin in e_pins:
			instance = RechargeCard.objects.create(network=network, denomination=denomination, pin=pin, reference = f"{website.prefix}-{gen_ref_id(14)}")
			print()
		msg = {"status": True, "message": "Successfully added."}
		return JsonResponse(msg)
	return render(request, "back/e_airtime.html")

def DelECard(request, pk):
	con = RechargeCard.objects.get(pk=pk)
	con.delete()
	return redirect("a_ecard")

def DeleteUsedCard(request):
	if is_ajax(request=request):
		card_type = request.GET['card_type']
		if card_type == 'e_cards':
			RechargeCard.objects.filter(status="Used").delete()
			msg = {"status": True, "message": "Successfully deleted."}
			return JsonResponse(msg)
		else:
			EPin.objects.filter(status="Used").delete()
			msg = {"status": True, "message": "Successfully deleted."}
			return JsonResponse(msg)

def AllEPins(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	pins = EPin.objects.all().filter(exams="WAEC")
	ctx = {
		"pins": pins
	}
	if is_ajax(request=request):
		card_type = request.GET['card_type']
		if card_type == 'e_cards':
			RechargeCard.objects.filter(status="Used").delete()
			msg = {"status": True, "message": "Successfully deleted."}
			return JsonResponse(msg)
		else:
			EPin.objects.filter(status="Used").delete()
			msg = {"status": True, "message": "Successfully deleted."}
			return JsonResponse(msg)
	return render(request, 'back/e_pin.html', ctx)

def AllEPinsNeco(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	pins = EPin.objects.all().filter(exams="NECO")
	ctx = {
		"pins": pins
	}
	if is_ajax(request=request):
		card_type = request.GET['card_type']
		if card_type == 'e_cards':
			RechargeCard.objects.filter(status="Used").delete()
			msg = {"status": True, "message": "Successfully deleted."}
			return JsonResponse(msg)
		else:
			EPin.objects.filter(status="Used").delete()
			msg = {"status": True, "message": "Successfully deleted."}
			return JsonResponse(msg)
	return render(request, 'back/e_pin_neco.html', ctx)

def DelEPin(request, pk):
	con = EPin.objects.get(pk=pk)
	con.delete()
	return redirect("a_epin")

def EPins(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	website = WebsiteConfig.objects.last()
	if is_ajax(request=request):
		exam = request.POST['exam']
		pins = request.POST['pins']
		e_pins = pins.split(",")
		for pin in e_pins:
			instance = EPin.objects.create(exams=exam, pin=pin, reference = f"{website.prefix}-{gen_ref_id(14)}")
			print()
		msg = {"status": True, "message": "Successfully added."}
		return JsonResponse(msg)
	return render(request, "back/e_pins.html")

def EPinSettings(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	epins = ECardSettings.objects.last()
	ctx = {
		'epins': epins
	}
	if is_ajax(request=request):
		form = EPinForm(request.POST)
		if form.is_valid():
			form.save()
			msg = {"status": True, "message": "Changes Saved Successfully."}
			return JsonResponse(msg)
		else:
			msg = {"status": False, "message": "Error Saving Data. Try again later."}
			return JsonResponse(msg)
	return render(request, "back/e_pin_settings.html", ctx)


def Transactions(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	transactions = Transaction.objects.all().order_by("-pk")
	ctx = {'transactions': transactions}
	return render(request, "back/transactions.html", ctx)

def TransactionDetail(request, ref):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	transaction = Transaction.objects.get(ps_ref=ref)
	ctx = {'tr': transaction, 'total': transaction.amount+transaction.fee}
	return render(request, "back/transaction.html", ctx)

def DelTransaction(request, ref):
	con = Transaction.objects.get(ps_ref=ref)
	con.delete()
	return redirect("a_transactions")

def WalletTransactions(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	transactions = WalletHistory.objects.all().order_by("-pk")
	ctx = {'transactions': transactions}
	return render(request, "back/wallet_history.html", ctx)

def WalletTransaction(request, ref):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	transaction = WalletHistory.objects.get(reference=ref)
	ctx = {'tr': transaction, 'total': transaction.amount+transaction.fee}
	return render(request, "back/wallethistory.html", ctx)

def DelWTransaction(request, ref):
	con = WalletHistory.objects.get(reference=ref)
	con.delete()
	return redirect("a_wallettransactions")

def Webhook(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	ctx = {
		"monnify_webhook": f"{request.scheme}://{request.META['HTTP_HOST']}/webhook/monnify/",
		"vtpass_webhook": f"{request.scheme}://{request.META['HTTP_HOST']}/webhook/vtpass/",
		"sme_webhook": f"{request.scheme}://{request.META['HTTP_HOST']}/webhook/sme/",
	}
	return render(request, "back/webhook.html", ctx)

def Logout(request):
	logout(request)
	return redirect("a_login")


def AddAdmin(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	if is_ajax(request=request):
		username = request.POST['username']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		mobile = request.POST['mobile']
		email = request.POST['email']
		staff_role = request.POST['staff_role']
		password = request.POST['password']

		check_username = User.objects.filter(username=username).exists()
		if check_username:
			msg = {"status": False, "message": "Username already exists."}
			return JsonResponse(msg)
		check_mobile = User.objects.filter(mobile=mobile).exists()
		if check_mobile:
			msg = {"status": False, "message": "Mobile Number already exists."}
			return JsonResponse(msg)
		check_email = User.objects.filter(email=email).exists()
		if check_email:
			msg = {"status": False, "message": "Email already exists."}
			return JsonResponse(msg)
		new_password = make_password(password)
		User.objects.create(
			username=username,
			first_name=first_name,
			last_name=last_name,
			mobile=mobile,
			email=email,
			staff_type=staff_role,
			is_staff=True,
			password=new_password
		)
		msg = {"status": True, "message": "Successfully Created."}
		return JsonResponse(msg)
	return render(request, "back/add_admin.html")

def DelStaff(request, username):
	con = User.objects.get(username=username)
	con.delete()
	return redirect("a_admins")


def Announcements(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	anns = Announcement.objects.all().order_by("-pk")
	if is_ajax(request=request):
		Announcement.objects.create(
			title=request.POST['title'],
			message=request.POST['message'],
			popup=request.POST['popup']
		)
		msg = {"status": True, "message": "Successfully Created."}
		return JsonResponse(msg)
	ctx = {
		'anns': anns
	}
	return render(request, "back/announcements.html", ctx)

def DelAnn(request, pk):
	Announcement.objects.filter(pk=pk).delete()
	return redirect("a_ann")

def AirtimeReq(request):
	anns = AirtimeRequest.objects.all().order_by("-pk")
	ctx = {
		'anns': anns
	}
	return render(request, "back/airtime-req.html", ctx)

def DelReq(request, pk):
	AirtimeRequest.objects.filter(pk=pk).delete()
	return redirect("a_req")


def NetworkSet(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	networks = NetworkList.objects.all()
	if is_ajax(request=request):
		check_network = NetworkList.objects.filter(slug=request.GET['slug']).exists()
		if check_network == False:
			msg = {"status": False, "message": "You may not be allowed to change anything else except from inactivity."}
			return JsonResponse(msg)
		network = NetworkList.objects.get(slug=request.GET['slug'])
		network.active = request.GET['active']
		network.save()
		msg = {"status": True, "message": "Updated Successfully."}
		return JsonResponse(msg)
	ctx = {
		"networks": networks
	}
	return render(request, "back/networks.html", ctx)

def NetworkSet(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	networks = NetworkList.objects.all()
	if is_ajax(request=request):
		check_network = NetworkList.objects.filter(slug=request.GET['slug']).exists()
		if check_network == False:
			msg = {"status": False, "message": "You may not be allowed to change anything else except from inactivity."}
			return JsonResponse(msg)
		network = NetworkList.objects.get(slug=request.GET['slug'])
		network.active = request.GET['active']
		network.save()
		msg = {"status": True, "message": "Updated Successfully."}
		return JsonResponse(msg)
	ctx = {
		"networks": networks
	}
	return render(request, "back/networks.html", ctx)

def DataPlug(request, net=None):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	if net == None:
		return redirect("a_networks")
	else:
		plans = DataPlan.objects.filter(network__slug=net)
	ctx = {
		"plans": plans,
		"network": net
	}
	if request.method == "POST":
		netw = NetworkList.objects.get(slug=request.POST['network'].lower())
		DataPlan.objects.create(
			pid=request.POST['plan_id'],
			network=netw,
			plan=request.POST['plan'],
			plan_type=request.POST['plan_type'],
			amount=request.POST['amount'],
			customer_price=request.POST['customer_price'],
			reseller_user_price=request.POST['reseller_price'],
			# api_user_price=request.POST['api_price'],
		)
		return redirect("a_data_plans", net)
	return render(request, "back/data-plans.html", ctx)

def fetchDataPlug(request, net=None):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	if net == None:
		return redirect("a_home")
	else:
		plans = fetchPlans(net)
		plan = plans['data']
		net = net
	
	if is_ajax(request=request):
		netw = NetworkList.objects.get(slug=request.GET['network'].lower())
		check_plan = DataPlan.objects.filter(pid=request.GET['pid']).exists()
		if check_plan == True:
			msg = {"status": False, "message": "Data Plan already exists. Please choose another."}
			return JsonResponse(msg)
		DataPlan.objects.create(
			pid=request.GET['pid'],
			network=netw,
			plan=request.GET['plan'],
			plan_type=request.GET['data_type'],
			amount=request.GET['amount'],
			customer_price=request.GET['customer_price'],
			reseller_user_price=request.GET['reseller_price'],
		)
		msg = {"status": True, "message": "Successfully added."}
		return JsonResponse(msg)
	ctx = {
		"plans": plan,
		"network": net
	}
	return render(request, "back/fetch_data.html", ctx)

def DeleteData(request, net=None, pid=None):
	dt = DataPlan.objects.filter(id=pid).delete()
	return redirect("a_data_plans", net)


def CablePlug(request, decoder=None):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	if decoder == None:
		return redirect("a_home")
	else:
		plans = CablePlan.objects.filter(decoder__slug=decoder)
	ctx = {
		"plans": plans,
		"decoder": decoder
	}
	if is_ajax(request=request):
		check_network = CablePlan.objects.filter(pid=request.GET['pid']).exists()
		if check_network == False:
			msg = {"status": False, "message": "You may not be allowed to change anything else except from plan name and inactivity."}
			return JsonResponse(msg)
		network = CablePlan.objects.get(pid=request.GET['pid'])
		network.active = request.GET['active']
		network.plan = request.GET['plan']
		network.customer_price = request.GET['customer_price']
		network.reseller_user_price = request.GET['reseller_price']
		network.api_user_price = request.GET['api_price']
		network.save()
		msg = {"status": True, "message": "Updated Successfully."}
		return JsonResponse(msg)
	return render(request, "back/cable-plans.html", ctx)


def fetchCablePlug(request, decoder=None):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	if decoder == None:
		return redirect("a_home")
	else:
		plans = TVBills(decoder)
		plan = plans['data']
		decoder = decoder
	
	if is_ajax(request=request):
		deco = CableList.objects.get(slug=request.GET['decoder'].lower())
		check_plan = CablePlan.objects.filter(pid=request.GET['variation_code']).exists()
		if check_plan == True:
			msg = {"status": False, "message": "Cable Plan already exists. Please choose another."}
			return JsonResponse(msg)
		CablePlan.objects.create(
			pid=request.GET['variation_code'],
			decoder=deco,
			plan=request.GET['name'],
			amount=request.GET['amount'],
			customer_price=request.GET['customer_price'],
			reseller_user_price=request.GET['reseller_price'],
			# api_user_price=request.GET['api_price'],
		)
		msg = {"status": True, "message": "Successfully added."}
		return JsonResponse(msg)
	ctx = {
		"plans": plan,
		"decoder": decoder
	}
	return render(request, "back/fetch_cable.html", ctx)


# Product Settings
def ProductSettings(request):
	if request.user.is_authenticated == False:
		return redirect("a_login")
	if request.user.is_authenticated and request.user.is_staff == False:
		logout(request)
		return redirect("a_login")
	pro = DataSetting.objects.last()
	ctx = {
		'pro': pro
	}
	if is_ajax(request=request):
		# print(request.POST)
		dstv = request.POST.get("dstv_is_active", None)
		gotv = request.POST.get("gotv_is_active", None)
		startimes = request.POST.get("startimes_is_active", None)
		disco = request.POST.get("disco_is_active", None)
		pro.dstv_is_active = False if dstv == None else True
		pro.gotv_is_active = False if gotv == None else True
		pro.startimes_is_active = False if startimes == None else True
		pro.disco_is_active = False if disco == None else True
		pro.save()
		msg = {"status": True, "message": "Updated Successfully."}
		return JsonResponse(msg)
	return render(request, "back/data-settings.html", ctx)


def CreateSuperUser(request):
	if is_ajax(request=request):
		username = request.POST['username']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		mobile = request.POST['mobile']
		email = request.POST['email']
		password = request.POST['password']

		check_username = User.objects.filter(username=username).exists()
		if check_username == True:
			msg = {"status": False, "message": "Username already exists."}
			return JsonResponse(msg)
		check_email = User.objects.filter(email=email).exists()
		if check_email == True:
			msg = {"status": False, "message": "Email already exists."}
			return JsonResponse(msg)
		check_mobile = User.objects.filter(mobile=mobile).exists()
		if check_mobile == True:
			msg = {"status": False, "message": "Mobile Number already exists."}
			return JsonResponse(msg)
		
		pwd = make_password(password)
		User.objects.create(
			username=username,
			first_name=first_name,
			last_name=last_name,
			email=email,
			mobile=mobile,
			password=pwd,
			is_staff=True,
			is_superuser=True,
			staff_type='Gold'
		)
		msg = {"status": True, "message": "Successfully Created."}
		return JsonResponse(msg)
	return render(request, "back/create-admin.html")
