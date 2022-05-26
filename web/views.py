from datetime import datetime as dt, timedelta
from decimal import Decimal
import json, math
from datetime import datetime
from rest_framework.authtoken.models import Token
import random
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from backbone.models import APISetting, AirtimeCommission, AirtimeRequest, AirtimeToCashCalc, Announcement, BillsCommission, ContactList, DataCommission, DataSetting, ECardSettings, EPin, RechargeCard, ReferralSystem, WebsiteConfig
from store.models import CableList, CablePlan, DataPlan, NetworkList
from transactions.models import Transaction, WalletHistory
from django.views.decorators.csrf import csrf_exempt
from utils.api import Monnify, PurchaseDisco, PurchaseTV, ValidateDisco, ValidateIUC, purchaseAirtime, purchaseData
from .models import User, UserBank, UserGenCard, UserGenPin, UserNotification, UserRef, UserVerify, Wallet
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from utils.functions import Banks, gen_key, gen_ref_id, is_ajax, validateMobile
from django.contrib.auth.hashers import make_password


# today = dt.date.today()
current_time = dt.now()

def error_404(request, exception):
    data = {}
    return  render(request, 'error404.html', data, status=404)

if current_time.hour < 12:
	greeting = "Good Morning"
elif 12 <= current_time.hour < 16:
	greeting = "Good Afternoon"
else:
	greeting = "Good Evening"

def Index(request):
	if request.GET:
		user_ref = request.GET['ref']
		request.session['referral'] = user_ref
	return render(request, "index.html")

def Home(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	wallet = Wallet.objects.get(user=request.user)
	banks = UserBank.objects.filter(user=request.user)
	color_list = ['primary', 'success', 'info', 'danger', 'secondary']
	refers = UserRef.objects.filter(referred_by=request.user)
	ref = ReferralSystem.objects.last()
	refers = UserRef.objects.filter(referred_by=request.user)
	refs = UserRef.objects.get(user=request.user)
	my_link = f"{request.scheme}://{request.META['HTTP_HOST']}?ref={refs.code}"
	notices = UserNotification.objects.filter(user=request.user).last()
	announcements = Announcement.objects.all().order_by("-pk")[:5]
	announcement = Announcement.objects.filter(popup=True).last()
	ctx = {
		'wallet': wallet,
		'banks': banks,
		'refers': refers,
		'color_list': color_list,
		'ref': ref,
		'my_link': my_link,
		'notice': notices,
		'greeting': greeting,
		'announcements': announcements,
		'announcement': announcement
	}
	if is_ajax(request=request):
		plan = request.POST['plan']
		wallet = Wallet.objects.get(user=request.user)
		website = WebsiteConfig.objects.last()
		if wallet.amount < website.reseller_price:
			msg = {"status": False, "message": "Insufficient fund. Please recharge."}
			return JsonResponse(msg)
		user = request.user
		user.user_type = plan
		user.save()
		wallet.amount -= website.reseller_price
		wallet.save()
		data = {}
		msg = {"status": True, "message": "Subscribed to Reseller Plan Successfully."}
		return JsonResponse(msg)
	return render(request, "home.html", ctx)


def Notifications(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	notices = UserNotification.objects.filter(user=request.user)
	ctx = {
		"notices": notices
	}
	return render(request, "notifications.html", ctx)

def FAQs(request):
	return render(request, "faqs.html")

@csrf_exempt
def Login(request):
	if request.user.is_authenticated:
		return redirect("home")
	if is_ajax(request=request):
		username = request.POST['username']
		password = request.POST['password']

		check_username = User.objects.filter(username=username).exists()
		if check_username == False:
			msg = {"status": False, "message": "Username is invalid"}
			return JsonResponse(msg)
		n_user = User.objects.get(username=username)
		if n_user.is_staff == True:
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
	return render(request, "login.html")

@csrf_exempt
def Register(request):
	if request.session.get('referral') == None:
		ref = None
	else:
		ref = request.session.get('referral')
	if is_ajax(request=request):
		username = request.POST['username']
		email = request.POST['email']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		mobile = request.POST['mobile']
		referral = request.POST.get("referral", None)
		password = request.POST['password']
		cpassword = request.POST['cpassword']
		if password != cpassword:
			msg = {"status": False, "message": "Password does not match."}
			return JsonResponse(msg)
		if mobile.startswith("+234"):
			m = mobile.lstrip("+234")
		elif mobile.startswith("234"):
			m = mobile.lstrip("234")
		elif mobile.startswith("0")== False:
			m = mobile
		else:
			m = mobile.lstrip("0")
		mobile = "0"+m
		whatsapp_number = f"234{m}"

		check_username = User.objects.filter(username=username).exists()
		if check_username == True:
			msg = {"status": False, "message": "Username is already in use"}
			return JsonResponse(msg)
		check_email = User.objects.filter(email=email).exists()
		if check_email == True:
			msg = {"status": False, "message": "Email is already in use"}
			return JsonResponse(msg)
		check_mobile = User.objects.filter(mobile=mobile).exists()
		if check_mobile:
			msg = {"status": False, "message": "Mobile Number already exists."}
			return JsonResponse(msg)
		if referral:
			check_ref2 = UserRef.objects.filter(code=referral).exists()
			if check_ref2 == False:
				msg = {"status": False, "message": "Invalid referral code. Try another or leave empty"}
				return JsonResponse(msg)
		new_password = make_password(password)
		otp_code = gen_key(6)
		website = WebsiteConfig.objects.last()
		instance = User.objects.create(
			first_name = first_name,
			last_name = last_name,
			mobile = mobile,
			username = username,
			email = email,
			is_active = True,
			password = new_password
		)
		website = WebsiteConfig.objects.last()
		ref = f"{website.prefix}-{gen_ref_id(8)}"
		vAccount = Monnify.VirtualAccount(f"{instance.username}", instance.email, ref)
		if vAccount['requestSuccessful'] == False:
			msg = {"status": False, "message": "There was an error verifying your account. Try in 30 minutes time."}
			return JsonResponse(msg)
		for ra in vAccount['responseBody']['accounts']:
			UserBank.objects.create(
				user=instance,
				bank_name=ra['bankName'],
				account_number=ra['accountNumber'],
				account_name=vAccount['responseBody']['customerName'],
				wallet_code=vAccount['responseBody']['accountReference']
			)
		Wallet.objects.create(user=instance)
		msg = {"status": True, "message": "Registration was successful. Kindly proceed to Login."}
		if referral:
			check_ref = UserRef.objects.filter(code=referral).exists()
			if check_ref:
				get_ref = UserRef.objects.get(code=referral)
				UserRef.objects.create(user=instance, referred_by=get_ref.user)
			else:
				UserRef.objects.create(user=instance)
		else:
			UserRef.objects.create(user=instance)
		return JsonResponse(msg)
	ctx = {
		'ref': ref
	}
	return render(request, "register.html", ctx)

@csrf_exempt
def VerifyAccount(request):
	if is_ajax(request=request):
		code = request.POST["otp"]
		username = request.POST["username"]

		check_username = User.objects.filter(username=username).exists()
		if check_username == False:
			msg = {"status": False, "message": "Username does not exists."}
			return JsonResponse(msg)
		check_code = UserVerify.objects.filter(token=code).exists()
		if check_code == False:
			msg = {"status": False, "message": "Code does not exists or has expired."}
			return JsonResponse(msg)
		get_code = UserVerify.objects.get(token=code)
		user = User.objects.get(username=username)
		user.is_active = True
		user.save()
		api = APISetting.objects.last()
		website = WebsiteConfig.objects.last()
		ref = f"{website.prefix}-{gen_ref_id(8)}"
		vAccount = Monnify.VirtualAccount(f"{user.username}", user.email, ref)
		if vAccount['requestSuccessful'] == False:
			msg = {"status": False, "message": "There was an error verifying your account. Try in 30 minutes time."}
			return JsonResponse(msg)
		for ra in vAccount['responseBody']['accounts']:
			UserBank.objects.create(
				user=user,
				bank_name=ra['bankName'],
				account_number=ra['accountNumber'],
				account_name=vAccount['responseBody']['customerName'],
				wallet_code=vAccount['responseBody']['accountReference']
			)
		Wallet.objects.create(user=user)
		get_code.delete()
		msg = {"status": True, "message": "Verify Successfully. Please wait while we redirect you."}
		return JsonResponse(msg)
	return render(request, "verify-account.html")

def ForgotPassword(request):
	if is_ajax(request=request):
		username = request.POST['username']
		check_username = User.objects.filter(username=username).exists()
		if check_username == False:
			msg = {"status": False, "message": "Username does not exists."}
			return JsonResponse(msg)
		# Send the message
		website = WebsiteConfig.objects.last()
		otp_code = gen_key(6)
		user = User.objects.get(username=username)
		check_code = UserVerify.objects.filter(user=user).exists()
		if check_code:
			ins = UserVerify.objects.filter(user=user).delete()
		mobile = user.mobile
		m = mobile.lstrip("0")
		mobile = "0"+m
		whatsapp_number = f"234{m}"
		message = f"Password Request.\n\n\n Hi {user.username}, \nYou have requested for password reset on {website.website_name},\n Your one-time verification code is *{otp_code}*\n\n This will be expired in 10 minutes.\n\nIf you have not made this request, kindly ignore.\n\n\n {website.website_name}"
		send_message_wa = DOJAH_API.SendWhatsApp(whatsapp_number, message)
		send_message_sms = DOJAH_API.SendSMS(whatsapp_number, message)
		UserVerify.objects.create(
            token=otp_code, user=user, expires_in=dt.now() + timedelta(minutes=70))
		msg = {"status": True, "message": "OTP Code sent to your Phone."}
		return JsonResponse(msg)
	return render(request, "forgot-password.html")

def ResetPassword(request):
	if is_ajax(request=request):
		otp = request.POST['otp']
		username = request.POST['username']
		password = request.POST['new_password']

		check_user = User.objects.filter(username=username).exists()
		if check_user == False:
			msg = {"status": False, "message": "Invalid Username"}
			return JsonResponse(msg)
		user = User.objects.get(username=username)
		check_code = UserVerify.objects.filter(token=otp, user=user).exists()
		if check_code == False:
			msg = {"status": False, "message": "Code is invalid or has expired"}
			return JsonResponse(msg)
		user.set_password(password)
		user.save()
		msg = {"status": True, "message": "Password has been reset."}
		return JsonResponse(msg)
	return render(request, "reset-password.html")

def Logout(request):
	logout(request)
	return redirect("login")

@csrf_exempt
def FundWalletBank(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	user = request.user
	wallet = Wallet.objects.get(user=request.user)
	banks = UserBank.objects.filter(user=request.user)
	bankList = Monnify.getBanks()
	allbanks = bankList['responseBody']
	color_list = ['primary', 'success', 'info', 'danger', 'secondary']
	ctx = {
		'wallet': wallet,
		'banks': banks,
		'allbanks': allbanks,
		'color_list': color_list
	}
	if is_ajax(request=request):
		bank_code = request.POST['bank']
		ref = f"G-{gen_ref_id(8)}"
		vAccount = Monnify.VirtualAccountNew(f"{user.username}", user.email, bank_code, ref)
		# print(vAccount)
		if vAccount['requestSuccessful'] == False:
			if "support" in vAccount['responseMessage']:
				msg = {"status": False, "message": "We do not support the selected bank. Please try again next time."}
				return JsonResponse(msg)
			else:
				msg = {"status": False, "message": "There was an error creating the account. Please try later."}
				return JsonResponse(msg)
		for ra in vAccount['responseBody']['accounts']:
			UserBank.objects.create(
				user=user,
				bank_name=ra['bankName'],
				account_number=ra['accountNumber'],
				account_name=vAccount['responseBody']['customerName'],
				wallet_code=vAccount['responseBody']['accountReference']
			)
		msg = {"status": True, "message": "Created Successfully"}
		return JsonResponse(msg)
	return render(request, "fund-bank.html", ctx)

@csrf_exempt
def FundWalletCard(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	api = APISetting.objects.last()
	website = WebsiteConfig.objects.last()
	ctx = {}
	if is_ajax(request=request):
		user = request.user
		amount = request.POST['amount']
		# charges = Decimal(amount) * (website.card_charges)
		# charge_amount = charges + Decimal(amount)
		ref = f"{website.prefix}-{gen_ref_id(14)}"
		data = {
			"email": user.email,
			"customer": f"{user.first_name} {user.last_name}",
			"amount": Decimal(amount),
			"api": api.monnify_api_key,
			"contract": api.monnify_contract_code,
			"ref": ref
		}
		wallet = Wallet.objects.get(user=request.user)
		WalletHistory.objects.create(
			user=user,
			reference = ref,
			amount = Decimal(amount),
			amount_after = wallet.amount,
			amount_before = wallet.amount,
			fee = Decimal(website.card_charges),
			method = "Card",
			trans_type = "Top-Up",
			credit = True,
			status = "pending"
		)
		msg = {"status": True, "message": "Successful", "data": data}
		return JsonResponse(msg)
	return render(request, "fund-card.html", ctx)


def FundWalletCardValidate(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	if is_ajax(request=request):
		ref = request.GET['ref']
		status = request.GET['status'].lower()


		check_ref = WalletHistory.objects.filter(reference=ref).exists()
		if check_ref == True:
			refs = WalletHistory.objects.get(reference=ref)
			if status == 'failed':
				refs.status = 'failed'
				refs.save()
				msg = {"status": True, "message": "Done"}
				return JsonResponse(msg)
			elif status == 'success':
				user_wallet = Wallet.objects.get(user=refs.user)
				add = refs.amount_after + refs.amount + refs.fee
				refs.amount_after = add
				refs.status = 'success'
				refs.ps_ref = request.GET['transaction_ref']
				bal = Decimal(refs.amount - refs.fee)
				user_wallet.amount += bal
				user_wallet.save()
				refs.save()
				msg = {"status": True, "message": "Done"}
				return JsonResponse(msg)
			else:
				refs.status = 'failed'
				refs.save()
				msg = {"status": True, "message": "Done"}
				return JsonResponse(msg)
		else:
			msg = {"status": False, "message": "Error"}
			return JsonResponse(msg)


def Pricing(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	bills = BillsCommission.objects.last()
	airtimes = AirtimeCommission.objects.last()
	datas = DataCommission.objects.last()
	ctx = {
		"airtimes": airtimes,
		"bills": bills,
		"datas": datas
	}
	return render(request, "pricing.html", ctx)

def Wallets(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	wallets = WalletHistory.objects.filter(user=request.user).order_by("-pk").prefetch_related("user")
	ctx = {
		"wallets": wallets
	}
	return render(request, "wallets.html", ctx)

def Transactions(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	transaction = Transaction.objects.filter(user=request.user).order_by("-pk").prefetch_related("user")
	ctx = {
		"transactions": transaction
	}
	return render(request, "transactions.html", ctx)

def ViewTransaction(request, ref=None):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	transaction = Transaction.objects.get(ps_ref=ref)
	total = transaction.amount + transaction.fee
	ctx = {
		"tr": transaction,
		"total": total
	}
	return render(request, "transaction.html", ctx)

@csrf_exempt
def AirtimeService(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	website = WebsiteConfig.objects.last()
	comm = AirtimeCommission.objects.last()
	
	if is_ajax(request=request):
		service_type = request.GET["service"]
		if service_type == 'check':
			network = request.GET['network']
			mobile = request.GET['mobile']
			number = validateMobile(mobile)
			if number == network:
				msg = {"status": True, "message": "Network Matched"}
				return JsonResponse(msg)
			else:
				msg = {"status": False, "message": "Network Does Not Match"}
				return JsonResponse(msg)
		elif service_type == "pay":
			amount = request.GET['amount']
			mobile = request.GET['mobile']
			network = request.GET['network']
			ported = request.GET['ported']
			ref = f"{website.prefix}-{gen_key(8)}"
			if network == 'MTN':
				if request.user.user_type == 'customer':
					interest = comm.mtn/100
				elif request.user.user_type == 'reseller':
					interest = comm.mtn_res/100
				else:
					interest = 0
				net = 1
			elif network == 'Glo':
				if request.user.user_type == 'customer':
					interest = comm.glo/100
				elif request.user.user_type == 'reseller':
					interest = comm.glo_res/100
				else:
					interest = 0
				net = 4
			elif network == 'Airtel':
				if request.user.user_type == 'customer':
					interest = comm.airtel/100
				elif request.user.user_type == 'reseller':
					interest = comm.airtel_res/100
				else:
					interest = 0
				net = 2
			else:
				if request.user.user_type == 'customer':
					interest = comm.etisalat/100
				elif request.user.user_type == 'reseller':
					interest = comm.etisalat_res/100
				else:
					interest = 0
				net = 3
			wallet = Wallet.objects.get(user=request.user)
			if wallet.amount < Decimal(amount):
				msg = {"status": False, "message": "Insufficient Funds. Please Recharge."}
				return JsonResponse(msg)
			purchase = purchaseAirtime(amount, net, mobile, ref)
			print(purchase)
			if purchase['status'] == False:
				if "Insufficient" in purchase['message']:
					msg = {"status": False, "message": "There was an error purchasing your airtime. Please try again later."}
					return JsonResponse(msg)
				elif "license" in purchase['message']:
					msg = {"status": False, "message": "There was an error making your purchase. Please Contact the Administrator"}
					return JsonResponse(msg)
				else:
					msg = {"status": False, "message": purchase['message']}
					return JsonResponse(msg)
			else:
				Transaction.objects.create(
					user=request.user,
					reference = purchase['data']['reference'],
					ps_ref = ref,
					amount = Decimal(amount),
					amount_before = wallet.amount,
					amount_after = wallet.amount - (Decimal(amount)),
					fee = Decimal("0.00"),
					method = f"{purchase['message']}",
					trans_type = f"Airtime",
					credit = False,
					status = "success"
				)
				wallet.amount -= Decimal(amount)
				wallet.bonus += Decimal(amount)*Decimal(interest)
				wallet.save()
				ref_sys = ReferralSystem.objects.last()
				if ref_sys.status == True:
					my_refer = UserRef.objects.get(user=request.user)
					if my_refer.referred_by != None:
						if my_refer.first_bonus == False:
							referral = my_refer.referred_by
							ref_wallet = Wallet.objects.get(user=referral)
							interest = ref_sys.referral_bonus/100
							bonus_point = interest*Decimal(amount)
							ref_wallet.bonus += bonus_point
							ref_wallet.save()
							my_refer.first_bonus = True
							my_refer.save()
				msg = {"status": True, "message": purchase['message']}
				return JsonResponse(msg)
	if request.user.user_type == 'reseller':
		mtn = (comm.mtn_res)
	else:
		mtn = comm.mtn
	if request.user.user_type == 'reseller':
		glo = (comm.glo_res)
	else:
		glo = comm.glo
	if request.user.user_type == 'reseller':
		airtel = (comm.airtel_res)
	else:
		airtel = comm.airtel
	if request.user.user_type == 'reseller':
		etisalat = (comm.etisalat_res)
	else:
		etisalat = comm.etisalat
	ctx = {
		"mtn": mtn,
		"glo": glo,
		"airtel": airtel,
		"etisalat": etisalat
	}
	return render(request, "airtime.html", ctx)


def LoadPlans(request):
	user = request.user
	if is_ajax(request=request):
		vvv = request.GET['datatype']
		if vvv == '':
			dataPlan = []
			if user.user_type == 'reseller':
				plans = DataPlan.objects.filter(network__slug=request.GET['network'], active=True).values('pid', 'network', 'plan', 'plan_type', 'reseller_user_price')
			else:
				plans = DataPlan.objects.filter(network__slug=request.GET['network'], active=True).values('pid', 'network', 'plan', 'plan_type', 'customer_price')
			
			for p in plans:
				dataPlans = {
					"id": p['pid'],
					"network": p['network'],
					"plan": p['plan'],
					"plan_type": p['plan_type'],
					'amount': p['reseller_user_price'] if user.user_type == 'reseller' else p['customer_price']
				}
				dataPlan.append(dataPlans)
			msg = {"status": True, "data": dataPlan}
			return JsonResponse(msg)
		else:
			dataPlan = []
			if user.user_type == 'reseller':
				plans = DataPlan.objects.filter(network__slug=request.GET['network'], plan_type=vvv, active=True).values('pid', 'network', 'plan', 'plan_type', 'reseller_user_price')
			else:
				plans = DataPlan.objects.filter(network__slug=request.GET['network'], plan_type=vvv, active=True).values('pid', 'network', 'plan', 'plan_type', 'customer_price')
			
			for p in plans:
				dataPlans = {
					"id": p['pid'],
					"network": p['network'],
					"plan": p['plan'],
					"plan_type": p['plan_type'],
					'amount': p['reseller_user_price'] if user.user_type == 'reseller' else p['customer_price']
				}
				dataPlan.append(dataPlans)
			msg = {"status": True, "data": dataPlan}
			return JsonResponse(msg)

@csrf_exempt
def DataService(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	website = WebsiteConfig.objects.last()
	nets = NetworkList.objects.all()
	user = request.user
	datasettings = DataSetting.objects.last()
	if is_ajax(request=request):
		network = request.GET['network']
		service_type = request.GET["service"]

		if service_type == 'check':
			mobile = request.GET["mobile"]
			number = validateMobile(mobile)
			if network == 'mtn':
				net = 'MTN'
			elif network == 'airtel':
				net = 'Airtel'
			elif network == '9mobile':
				net = '9mobile'
			elif network == 'glo':
				net = 'Glo'
			if number == net:
				msg = {"status": True, "message": "Network Matched"}
				return JsonResponse(msg)
			else:
				msg = {"status": False, "message": "Network Does Not Match"}
				return JsonResponse(msg)
		elif service_type == 'pay':
			plan = request.GET["plan"]
			mobile = request.GET["mobile"]
			pr = DataPlan.objects.filter(network__slug=request.GET['network'], pid=plan).last()
			amount = pr.reseller_user_price if user.user_type == 'reseller' else pr.customer_price
			ref = f"{website.prefix}-{gen_key(8)}"
			wallet = Wallet.objects.get(user=request.user)
			if wallet.amount < Decimal(amount):
				msg = {"status": False, "message": "Insufficient Funds. Please Recharge."}
				return JsonResponse(msg)
			pl = DataPlan.objects.get(pid=plan)
			purchase = purchaseData(plan, network, mobile, ref)
			print(purchase)
			if user.user_type == 'reseller':
				price = pl.reseller_user_price
			else:
				price = pl.customer_price
			if purchase['status'] == False:
				if "fund" in purchase['message']:
					msg = {"status": False, "message": "There was an error purchasing your data plan. Please try again later."}
					return JsonResponse(msg)
				elif "insufficient" in purchase['message']:
					msg = {"status": False, "message": "There was an error making your purchase. Please Contact the Administrator"}
					return JsonResponse(msg)
				else:
					msg = {"status": False, "message": purchase['message']}
					return JsonResponse(msg)
			else:
				Transaction.objects.create(
					user=request.user,
					reference = purchase['data']['reference'],
					ps_ref = ref,
					amount = Decimal(price),
					amount_before = wallet.amount,
					amount_after = wallet.amount - (Decimal(price)),
					fee = Decimal("0.00"),
					method = f"{purchase['message']}",
					trans_type = f"Data",
					credit = False,
					status = "success"
				)
				wallet.amount -= Decimal(price)
				wallet.save()
				ref_sys = ReferralSystem.objects.last()
				my_refer = UserRef.objects.get(user=request.user)
				if ref_sys.status == True:
					my_refer = UserRef.objects.get(user=request.user)
					if my_refer.referred_by != None:
						if my_refer.first_bonus == False:
							referral = my_refer.referred_by
							ref_wallet = Wallet.objects.get(user=referral)
							interest = ref_sys.referral_bonus/100
							bonus_point = interest*Decimal(amount)
							ref_wallet.bonus += bonus_point
							ref_wallet.save()
							my_refer.first_bonus = True
							my_refer.save()
				msg = {"status": True, "message": purchase['message']}
				return JsonResponse(msg)
	ctx = {
		"datasettings": datasettings,
		"nets": nets
	}
	return render(request, "datas.html", ctx)

@csrf_exempt
def TVBillsPayment(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	website = WebsiteConfig.objects.last()
	user = request.user
	# comm = BillsCommission.objects.last()
	if is_ajax(request=request):
		decoder = request.GET['decoder']
		service_type = request.GET["service"]

		if service_type == 'package':
			if user.user_type == 'reseller':
				plans = CablePlan.objects.filter(decoder__slug=decoder, active=True).values('pid', 'decoder', 'plan', 'reseller_user_price')
			else:
				plans = CablePlan.objects.filter(decoder__slug=decoder, active=True).values('pid', 'decoder', 'plan', 'customer_price')
			
			dataPlan = []
			for p in plans:
				dataPlans = {
					"pid": p['pid'],
					"decoder": p['decoder'],
					"plan": p['plan'],
					'amount': p['reseller_user_price'] if user.user_type == 'reseller' else p['customer_price']
				}
				dataPlan.append(dataPlans)
			msg = {"status": True, "data": dataPlan}
			return JsonResponse(msg)
		elif service_type == 'validate':
			iuc = request.GET["iuc"]
			verify = ValidateIUC(decoder.lower(), iuc)
			msg = {"status": True, "data": verify['data']}
			return JsonResponse(msg)
		elif service_type == 'purchase':
			iuc = request.GET["iuc"]
			decoder = request.GET["decoder"]
			cphone = request.GET["cphone"]
			package = request.GET["package"]
			price = request.GET["amount"]
			amount = price.split("₦")[1]
			ref = f"{datetime.today().strftime('%Y%m%d%H%M')}{website.prefix}"
			wallet = Wallet.objects.get(user=request.user)
			if wallet.amount < Decimal(amount):
				msg = {"status": False, "message": "Insufficient Funds. Please Recharge."}
				return JsonResponse(msg)
			purchase = PurchaseTV(decoder, iuc, package, cphone, amount, ref)
			print(purchase)
			if purchase['status'] == True:
				Transaction.objects.create(
					user=request.user,
					reference = purchase['data']['reference'],
					ps_ref = ref,
					amount = Decimal(amount),
					amount_before = wallet.amount,
					amount_after = wallet.amount - (Decimal(amount)),
					fee = Decimal("0.00"),
					method = f"{decoder.upper()} - {package}",
					trans_type = f"Cable TV",
					credit = False,
					status = "success"
				)
				wallet.amount -= Decimal(amount)
				wallet.save()
				ref_sys = ReferralSystem.objects.last()
				if ref_sys.status == True:
					my_refer = UserRef.objects.get(user=request.user)
					if my_refer.referred_by != None:
						if my_refer.first_bonus == False:
							referral = my_refer.referred_by
							ref_wallet = Wallet.objects.get(user=referral)
							interest = ref_sys.referral_bonus/100
							bonus_point = interest*Decimal(amount)
							ref_wallet.bonus += bonus_point
							ref_wallet.save()
							my_refer.first_bonus = True
							my_refer.save()
				msg = {"status": True, "message": f"{purchase['message']}"}
				return JsonResponse(msg)
			elif 'fund' in purchase['message']:
				msg = {"status": False, "message": "There was an error making purchase. Try again later."}
				return JsonResponse(msg)
			else:
				msg = {"status": False, "message": purchase['message']}
				return JsonResponse(msg)
	
	deco = CableList.objects.filter(active=True)
	ctx = {
		"decos": deco
	}
	return render(request, "tv-bills.html", ctx)

@csrf_exempt
def MetreBillsPayment(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	website = WebsiteConfig.objects.last()
	comm = BillsCommission.objects.last()
	pro = DataSetting.objects.last()
	if pro.disco_is_active == False:
		return redirect("home")
	if is_ajax(request=request):
		service_type = request.GET["service"]

		if service_type == 'validate':
			disco = request.GET['disco']
			iuc = request.GET["iuc"]
			disco_type = request.GET["disco_type"]
			verify = ValidateDisco(disco, disco_type, iuc)
			if verify['status'] == False:
				msg = {"status": False, "message": verify['message']}
				return JsonResponse(msg)
			else:
				msg = {"status": True, "data": verify['data']}
				return JsonResponse(msg)
		elif service_type == 'purchase':
			iuc = request.GET["cname"]
			decoder = request.GET["decoder"]
			cphone = request.GET["iuc"]
			package = request.GET["package"]
			amount = request.GET["amount"]
			ref = f"{datetime.today().strftime('%Y%m%d%H%M')}{website.prefix}"
			wallet = Wallet.objects.get(user=request.user)
			if wallet.amount < Decimal(amount):
				msg = {"status": False, "message": "Insufficient Funds. Please Recharge."}
				return JsonResponse(msg)
			purchase = PurchaseDisco(decoder, package, iuc, cphone, amount, ref)
			if purchase['status'] == True:
				Transaction.objects.create(
					user=request.user,
					reference = purchase['data']['reference'],
					ps_ref = ref,
					amount = purchase['data']['amount'],
					amount_before = wallet.amount,
					amount_after = wallet.amount - (Decimal(purchase["data"]["amount"])),
					fee = Decimal("0.00"),
					method = f"{decoder.upper() - {package.upper()}}",
					trans_type = f"Disco",
					credit = False,
					status = "success"
				)
				if request.user.user_type == 'reseller':
					interest = comm.edc_res/100
				else:
					interest = comm.edc/100
				wallet.amount -= Decimal(purchase['amount']['amount'])
				wallet.bonus += Decimal(amount)*Decimal(interest)
				wallet.save()
				ref_sys = ReferralSystem.objects.last()
				if ref_sys.status == True:
					my_refer = UserRef.objects.get(user=request.user)
					if my_refer.referred_by != None:
						if my_refer.first_bonus == False:
							referral = my_refer.referred_by
							ref_wallet = Wallet.objects.get(user=referral)
							interest = ref_sys.referral_bonus/100
							bonus_point = interest*Decimal(amount)
							ref_wallet.bonus += bonus_point
							ref_wallet.save()
							my_refer.first_bonus = True
							my_refer.save()
				msg = {"status": True, "message": f"{purchase['message']}"}
				return JsonResponse(msg)
			elif 'fund' in purchase['message']:
				msg = {"status": False, "message": "There was an error making purchase. Try again later."}
				return JsonResponse(msg)
			else:
				msg = {"status": False, "message": purchase['message']}
				return JsonResponse(msg)
	if request.user.user_type == 'customer':
		edc = (comm.edc)
	elif request.user.user_type == 'reseller':
		edc = comm.edc_res
	ctx = {
		"electricity": edc
	}
	return render(request, "metre.html", ctx)

@csrf_exempt
def SmileNetwork(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	smile = VTPass.SmilePlan()
	ctx = {
		"smile": smile['content']['variations']
	}
	if is_ajax(request=request):
		mobile_number = request.GET['mobile_number']
		service_type = request.GET["service"]

		if service_type == 'validate':
			verify = VTPass.ValidateSmile(mobile_number)
			print(verify)
			msg = {"status": True, "data": verify['content']}
			return JsonResponse(msg)
	return render(request, "smile.html", ctx)

@csrf_exempt
def Setting(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	banks = Banks()
	if is_ajax(request=request):
		action = request.POST['action']
		if action == 'password':
			old_password = request.POST['old_password']
			new_password = request.POST['new_password']
			new_password_2 = request.POST['new_password_2']

			user_password = request.user.check_password(old_password)
			if user_password == False:
				msg = {"status": False, "message": "Current Password is incorrect"}
				return JsonResponse(msg)
			elif new_password != new_password_2:
				msg = {"status": False, "message": "Password do not match."}
				return JsonResponse(msg)
			else:
				request.user.set_password(new_password)
				request.user.save()
				update_session_auth_hash(request, request.user)
				msg = {"status": True, "message": "Password has been updated"}
				return JsonResponse(msg)
	ctx = {
		"banks": banks
	}
	return render(request, "settings.html", ctx)

def SetPin(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	if is_ajax(request=request):
		action = request.POST['action']
		if action == 'pin':
			pin = request.POST['new_pin']
			password = request.POST['password']

			user_password = request.user.check_password(password)
			if user_password == False:
				msg = {"status": False, "message": "Password is incorrect"}
				return JsonResponse(msg)
			else:
				request.user.transaction_pin = pin
				request.user.save()
				msg = {"status": True, "message": "Pin has been updated"}
				return JsonResponse(msg)
	return render(request, "set_pin.html")

@csrf_exempt
def FetchNuban(request):
	if is_ajax(request=request):
		account_number = request.GET['account_number']
		bank_code = request.GET['bank_code']
		v = DOJAH_API.resolveNuban(account_number, bank_code)
		data = {
			"account_name": v['entity']['account_name']
		}
		msg = {"status": True, "message": "Successful", "data": data}
		return JsonResponse(msg)

@csrf_exempt
def UpdateBank(request):
	if is_ajax(request=request):
		bank_name = request.POST['bank_name']
		account_number = request.POST['account_number']
		account_name = request.POST['account_name']
		user = request.user
		user.account_name = account_name
		user.account_number = account_number
		user.bank_name = bank_name
		user.bank_set = True
		user.save()
		msg = {"status": True, "message": "Bank Details Updated Successfully"}
		return JsonResponse(msg)


@csrf_exempt
def BonusToWallet(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	bonus = Wallet.objects.get(user=request.user)
	website = WebsiteConfig.objects.last()
	ctx = {
		"bonus": bonus.bonus
	}
	if is_ajax(request=request):
		amount = request.POST['amount']
		if Decimal(amount) > bonus.bonus:
			msg = {"status": False, "message": "Insufficient amount in bonus."}
			return JsonResponse(msg)
		elif Decimal(amount) < website.min_bonus_transfer:
			msg = {"status": False, "message": "You can only transfer 100 and above."}
			return JsonResponse(msg)
		else:
			bonus.bonus -= Decimal(amount)
			bonus.amount += Decimal(amount)
			bonus.save()
			msg = {"status": True, "message": "Transferred was successful."}
			return JsonResponse(msg)
	return render(request, "bonus-wallet.html", ctx)

@csrf_exempt
def AirtimeToCash(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	if request.user.bank_set == False:
		return redirect("settings")
	website = WebsiteConfig.objects.last()
	a2c = AirtimeToCashCalc.objects.last()
	if is_ajax(request=request):
		body = json.loads(request.body)
		network = body['network']
		mobile = body['mobile']
		amount = body['amount']
		fund_type= body['send_to']
		amount_send = body['amount_send']

		if fund_type == "Fund Wallet":
			send_to = f"fund his/her wallet with {amount_send}."
		else:
			send_to = f"send {amount_send} to his/her bank account.\n\n\nAccount Name:{request.user.account_name}\n\n\nAccount Number: {request.user.account_number}\n\n\nBank Name: {request.user.bank_name}"
		message = f"Dear {website.website_name},\n\n*{request.user.username}* has just sold ₦{amount} {network} airtime to you from this number *{mobile}* and has asked to {send_to}\n\n\nThanks."
		msg2 = f"Dear {website.website_name}, {request.user.username} has just sold ₦{amount} {network} airtime to you from this number {mobile} and has asked to {send_to}.   Thanks."
		number = a2c.notification_number
		if number.startswith("+234"):
			m = number.lstrip("+234")
		elif number.startswith("234"):
			m = number.lstrip("234")
		elif number.startswith("0")== False:
			m = number
		else:
			m = number.lstrip("0")
		number = "0"+m
		whatsapp_number = f"234{m}"
		send_amount = amount_send.split("₦")[1]
		fee = Decimal(amount) - Decimal(send_amount)
		Transaction.objects.create(
			user= request.user,
			reference = f"{website.prefix}-{gen_ref_id(8)}",
			ps_ref = f"{website.prefix}-{gen_ref_id(8)}",
			amount = Decimal(amount),
			fee = fee,
			method = f"Airtime Sell",
			trans_type = f"Airtime To Cash",
			credit = False,
			status = "success"
		)
		AirtimeRequest.objects.create(
			method=fund_type,
			user=request.user,
			amount=Decimal(amount),
			cash_back=fee,
			mobile=f"{mobile} - {network}"
		)
		DOJAH_API.SendWhatsApp(whatsapp_number, message)
		DOJAH_API.SendSMS(whatsapp_number, msg2)
		msg = {"status": True, "message": "You will be notified once confirmed."}
		return JsonResponse(msg)
	return render(request, "airtime-to-cash.html")

def RechargeCardPrint(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	pin_price = ECardSettings.objects.last()
	if request.user.user_type == 'reseller':
		mtn_price = pin_price.mtn_discount_res
	else:
		mtn_price = pin_price.mtn_discount_users
	if request.user.user_type == 'reseller':
		glo_price = pin_price.glo_discount_res
	else:
		glo_price = pin_price.glo_discount_users
	if request.user.user_type == 'reseller':
		airtel_price = pin_price.airtel_discount_res
	else:
		airtel_price = pin_price.airtel_discount_users
	if request.user.user_type == 'reseller':
		etisalat_price = pin_price.etisalat_discount_res
	else:
		etisalat_price = pin_price.etisalat_discount_users
	ctx = {
		"mtn_price": mtn_price,
		"glo_price": glo_price,
		"airtel_price": airtel_price,
		"etisalat_price": etisalat_price,
	}
	if is_ajax(request=request):
		network = request.POST['network']
		denomination = request.POST['denomination']
		quantity = request.POST['quantity']
		if int(quantity) < 1:
			msg = {"status": False, "message": "Please enter at least 1 quantity"}
			return JsonResponse(msg)
		cards = RechargeCard.objects.filter(network=network, denomination=denomination).exclude(status="Used")
		if int(quantity) > len(cards):
			msg = {"status": False, "message": f"We are sorry, We only have {len(cards)} quantity left."}
			return JsonResponse(msg)
		if network == "MTN":
			price = mtn_price
		elif network == "GLO":
			price = glo_price
		elif network == "Airtel":
			price = airtel_price
		else:
			price = etisalat_price
		inte = (((price/100)*int(denomination)))
		amount = ((int(denomination) - inte)*int(quantity))
		wallet = Wallet.objects.get(user=request.user)
		if wallet.amount < Decimal(amount):
			msg = {"status": False, "message": f"Insufficient funds. Please recharge and try again."}
			return JsonResponse(msg)
		unused_cards = RechargeCard.objects.filter(network=network, denomination=denomination).exclude(status="Used")[:int(quantity)]
		for c in unused_cards:
			UserGenCard.objects.create(
				user=request.user,
				reference=c.reference,
				pin=c.pin,
				denomination=c.denomination,
				network=c.network
			)
			c.status = "Used"
			c.save()
			print()
		wallet.amount -= Decimal(amount)
		wallet.save()
		website = WebsiteConfig.objects.last()
		Transaction.objects.create(
			user=request.user,
			reference = f"{website.prefix}-{gen_key(8)}",
			ps_ref = f"{website.prefix}-{gen_key(8)}",
			amount = Decimal(amount),
			fee = Decimal("0.00"),
			method = f"{quantity}pc(s) of {denomination} Airtime Generated",
			trans_type = f"E-Recharge Generate",
			credit = False,
			status = "success"
		)
		msg = {"status": True, "message": f"Airtime(s) Generated"}
		return JsonResponse(msg)
	return render(request, "recharge-card.html", ctx)

def FetchCardDenomination(request):
	if is_ajax(request=request):
		network = request.GET['network']
		cards = RechargeCard.objects.filter(network=network)
		count_cards = len(cards)
		data = []
		for d in cards:
			datas = {
				"reference": d.reference,
				"network": d.network,
				"denomination": d.denomination,
				"status": d.status,
				"date": d.date
			}
			data.append(datas)
		msg = {"status": True, "message": "Okay", "data": data, "count_cards": count_cards}
		return JsonResponse(msg)

def myReferral(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	refers = UserRef.objects.filter(referred_by=request.user).prefetch_related("user")
	ref = UserRef.objects.get(user=request.user)
	my_link = f"{request.scheme}://{request.META['HTTP_HOST']}?ref={ref.code}"
	ctx = {
		'refers': refers,
		'link': my_link
	}
	return render(request, "refers.html", ctx)

def Conts(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	contacts = ContactList.objects.all()
	ctx = {
		'contacts': contacts
	}
	return render(request, "contacts.html", ctx)


def ResultChecker(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	wpins = EPin.objects.filter(exams="WAEC").exclude(status="Used")
	npins = EPin.objects.filter(exams="NECO").exclude(status="Used")
	pin_price = ECardSettings.objects.last()
	if request.user.user_type == 'resellers':
		waec_price = pin_price.waec_price_res
	else:
		waec_price = pin_price.waec_price_users
	if request.user.user_type == 'reseller':
		neco_price = pin_price.neco_price_res
	else:
		neco_price = pin_price.neco_price_users
	ctx = {
		'npins': npins,
		'wpins': wpins,
		'neco_price': neco_price,
		'waec_price': waec_price
	}

	if is_ajax(request=request):
		service = request.POST['exams']
		qty = request.POST['quantity']

		if service == "WAEC":
			amount = waec_price
		else:
			amount = neco_price
		
		total_price = int(qty)*Decimal(amount)
		website = WebsiteConfig.objects.last()
		wallet = Wallet.objects.get(user=request.user)
		if int(qty) < 1:
			msg = {"status": False, "message": "Please enter at least 1 quantity"}
			return JsonResponse(msg)
		if wallet.amount < total_price:
			msg = {"status": False, "message": "Insufficient funds. Please recharge and try again."}
			return JsonResponse(msg)
		cards = EPin.objects.filter(exams=service).exclude(status="Used")
		if int(qty) > len(cards):
			msg = {"status": False, "message": f"We are sorry, We only have {len(cards)} quantity left."}
			return JsonResponse(msg)
		unused_cards = EPin.objects.filter(exams=service).exclude(status="Used")[:int(qty)]
		for c in unused_cards:
			UserGenPin.objects.create(
				user=request.user,
				reference=c.reference,
				pin=c.pin,
				exams=c.exams
			)
			c.status = "Used"
			c.save()
			print()
		wallet.amount -= Decimal(total_price)
		wallet.save()
		Transaction.objects.create(
			user=request.user,
			reference = f"{website.prefix}-{gen_key(8)}",
			ps_ref = f"{website.prefix}-{gen_key(8)}",
			amount = Decimal(amount),
			fee = Decimal("0.00"),
			method = f"{qty}pc(s) of {service} Pin Generated",
			trans_type = f"E-Pins Generate",
			credit = False,
			status = "success"
		)
		msg = {"status": True, "message": f"E-Pin(s) Generated"}
		return JsonResponse(msg)
	return render(request, "result-checker.html", ctx)

def myEPins(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	pins = UserGenPin.objects.filter(user=request.user).prefetch_related("user")
	ctx = {
		"pins": pins
	}
	if is_ajax(request=request):
		pk = request.GET['pk']
		user_card = UserGenPin.objects.get(pk=pk)
		user_card.delete()
		msg = {"status": True}
		return JsonResponse(msg)
	return render(request, "my_epins.html", ctx)

def myCards(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	pins = UserGenCard.objects.filter(user=request.user).prefetch_related("user")
	ctx = {
		"pins": pins
	}
	if is_ajax(request=request):
		pk = request.GET['pk']
		user_card = UserGenCard.objects.get(pk=pk)
		user_card.delete()
		msg = {"status": True}
		return JsonResponse(msg)
	return render(request, "my_ecards.html", ctx)

def printAirtime(request, pk):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	card = UserGenCard.objects.get(pk=pk)
	ctx = {
		"tr": card
	}
	return render(request, "e_airtime_rec.html", ctx)

def DelMyCard(request, pk):
	user_card = UserGenCard.objects.get(pk=pk)
	user_card.delete()
	return redirect("cards")

def DelMyPin(request, pk):
	user_card = UserGenPin.objects.get(pk=pk)
	user_card.delete()
	return redirect("epins")

def DeveloperPage(request):
	if request.user.is_authenticated == False:
		return redirect("login")
	if request.user.is_staff == True:
		return redirect("a_home")
	if request.user.user_type != "api":
		return redirect("home")
	
	token = Token.objects.get(user=request.user)
	datas = DataPlan.objects.all()
	cables = CableList.objects.all()
	cable_list = CablePlan.objects.all()
	ctx = {
		"token": token,
		"datas": datas,
		"cables": cables,
		"cable_list": cable_list
	}
	return render(request, "documentation.html", ctx)


@csrf_exempt
def MonnifyWebhook(request):
	website = WebsiteConfig.objects.last()
	r = json.loads(request.body)
	user_bank = UserBank.objects.filter(wallet_code=r['eventData']['reference']).last()
	user_wallet = Wallet.objects.get(user=user_bank.user)
	bal = Decimal(r['eventData']['amountPaid']) - website.transfer_charges
	user_wallet.amount += bal
	user_wallet.save()
	WalletHistory.objects.create(
		user = user_wallet.user,
		reference = r['eventData']['transactionReference'],
		ps_ref =  r['eventData']['paymentReference'],
		amount =  Decimal(r['eventData']['amountPaid']),
		amount_before = user_wallet.amount - Decimal(r['eventData']['amountPaid']),
		amount_after = user_wallet.amount + Decimal(r['eventData']['amountPaid']),
		credit = True,
		fee = website.transfer_charges,
		method = "Bank Transfer",
		trans_type= "Top-Up",
		status = "success"
	)
	UserNotification.objects.create(user=user_wallet.user,title=f"Monnify Payment successful. Your account has been credited with sum of ₦{bal}.")
	return HttpResponse("Cool")


@csrf_exempt
def SMEPlugWebhook(request):
	r = json.loads(request.body)
	print(r)
	if r['transaction']['status'] != 'success':
		reference = r['transaction']['reference']
		tr = Transaction.objects.get(reference=reference)
		wallet = Wallet.objects.get(user=tr.user)
		tr.status = 'failed'
		tr.save()
		wallet.amount += Decimal(r['transaction']['price'])
		wallet.amount_before -= Decimal(r['transaction']['price'])
		wallet.amount_after += Decimal(r['transaction']['price'])
		wallet.save()
		return HttpResponse("Done")
	else:
		return HttpResponse("Done")

@csrf_exempt
def VTPassWebhook(request):
	website = WebsiteConfig.objects.last()
	r = json.loads(request.body)
	print(r)
	if r['type'] == 'transaction-update':
		if r['data']['content'] != 'delivered':
			reference = r['data']['requestId']
			tr = Transaction.objects.get(ps_ref=reference)
			wallet = Wallet.objects.get(user=tr.user)
			tr.status = 'failed'
			tr.save()
			wallet.amount += Decimal(r['data']['content']['amount'])
			wallet.amount_before -= Decimal(r['content']['amount'])
			wallet.amount_after += Decimal(r['content']['amount'])
			wallet.save()
			return HttpResponse("Done")
		else:
			return HttpResponse("Done")
	else:
		return HttpResponse("Done")
