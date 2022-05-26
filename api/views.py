from decimal import Decimal
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.serializers import TransactionSerializer
from backbone.models import AirtimeCommission, BillsCommission, DataCommission, DataSetting, ReferralSystem, WebsiteConfig
from store.models import CablePlan, DataPlan
from transactions.models import Transaction
from utils.api import DOJAH_API, SME, VTPass
from utils.functions import gen_key
from web.models import UserRef, Wallet
from datetime import datetime


website = WebsiteConfig.objects.last()
data_settings = DataSetting.objects.last()

class Transactions(APIView):
	serializer_class = TransactionSerializer
	def get(self, request, ref=None):
		if ref == None:
			data = Transaction.objects.filter(user=request.user).prefetch_related("user")
			serializer = self.serializer_class(data, many=True)
			return Response({"status": True, "message": "Transactions Queried Successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
		else:
			check_ref = Transaction.objects.filter(ps_ref=ref).exists()
			if check_ref == False:
				return Response({"status": False, "message": "Incorrect Reference Provided."}, status=status.HTTP_404_NOT_FOUND)
			data = Transaction.objects.get(ps_ref=ref)
			serializer = self.serializer_class(data, many=False)
			return Response({"status": True, "message": "Transactions Queried Successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

class DataPlans(APIView):
	def get(self, request, network=None):
		try:
			user = request.user
			# plans = SME.fetchPlans()
			if network == None:
				if user.user_type == 'api':
					plans = DataPlan.objects.filter(active=True).values('pid', 'network', 'plan', 'plan_type', 'api_user_price')
				else:
					plans = DataPlan.objects.filter(active=True).values('pid', 'network', 'plan', 'plan_type', 'vendor_user_price')
			else:
				if user.user_type == 'api':
					plans = DataPlan.objects.filter(network__slug=network, active=True).values('pid', 'network', 'plan', 'plan_type', 'api_user_price')
				else:
					plans = DataPlan.objects.filter(network__slug=network, active=True).values('pid', 'network', 'plan', 'plan_type', 'vendor_user_price')
			
			dataPlan = []
			for p in plans:
				dataPlans = {
					"id": p['pid'],
					"network": p['network'],
					"plan": p['plan'],
					"plan_type": p['plan_type'],
					'amount': p['api_user_price'] if user.user_type == 'api' else p['vendor_user_price']
				}
				dataPlan.append(dataPlans)
			return Response({"status": True, "message": "Data Queried Successfully", "data": dataPlan}, status=status.HTTP_200_OK)
		except:
			return Response({"status": False, "message": "There was an error fetching data plans from the server. Please contact the Administrator."}, status=status.HTTP_400_BAD_REQUEST)
	
	def post(self, request):
		try:
			network = request.data.get("network", None)
			mobile_number = request.data.get("mobile_number", None)
			plan = request.data.get("plan", None)
			wallet = Wallet.objects.get(user=request.user)
			data_plan = DataPlan.objects.get(pid=plan)
			user = request.user
			if user.user_type == 'vendor':
				price = data_plan.vendor_user_price
			else:
				price = data_plan.api_user_price
			ref = f"{website.prefix}-{gen_key(8)}"
			if wallet.amount < Decimal(price):
				return Response({"status": False, "message": "Insufficient funds. Please recharge and try again."}, status=status.HTTP_402_PAYMENT_REQUIRED)
			purchase = SME.purchaseDataAPI(data_plan.pid, network, mobile_number, ref)
			comm = DataCommission.objects.last()
			if network == '1':
				if request.user.user_type == 'vendor':
					interest = comm.mtn_ven/100
				elif request.user.user_type == 'api':
					interest = comm.mtn_api/100
				else:
					interest = 0
				net = 'MTN'
			elif network == '2':
				if request.user.user_type == 'vendor':
					interest = comm.airtel_ven/100
				elif request.user.user_type == 'api':
					interest = comm.airtel_api/100
				else:
					interest = 0
				net = 'Airtel'
			elif network == '3':
				if request.user.user_type == 'vendor':
					interest = comm.etisalat_ven/100
				elif request.user.user_type == 'api':
					interest = comm.etisalat_api/100
				else:
					interest = 0
				net = '9mobile'
			elif network == '4':
				if request.user.user_type == 'vendor':
					interest = comm.glo_ven/100
				elif request.user.user_type == 'api':
					interest = comm.glo_api/100
				else:
					interest = 0
				net = 'Glo'
			
			if purchase['status'] == False:
				if "wallet" in purchase['msg']:
					return Response({"status": False, "message": "There was an error purchasing your data plan. Please try again later."}, status=status.HTTP_400_BAD_REQUEST)
				elif "Insufficient" in purchase["msg"]:
					DOJAH_API.SendSMS(website.whatsapp_number, purchase["msg"])
					DOJAH_API.SendWhatsApp(website.whatsapp_number, purchase["msg"])
					return Response({"status": False, "message": "There was an error purchasing your data plan. Report to the Administrator"}, status=status.HTTP_400_BAD_REQUEST)
				elif "license" in purchase["msg"]:
					DOJAH_API.SendSMS(website.whatsapp_number, f"{purchase['msg']} - SMEPlug")
					DOJAH_API.SendWhatsApp(website.whatsapp_number, f"{purchase['msg']} - SMEPlug")
					return Response({"status": False, "message": "An unknown error occurred. Please contact the Administrator."}, status=status.HTTP_400_BAD_REQUEST)
				else:
					return Response({"status": False, "message": purchase['msg']}, status=status.HTTP_400_BAD_REQUEST)
			else:
				Transaction.objects.create(
					user=request.user,
					reference = purchase['data']['reference'],
					ps_ref = ref,
					amount = Decimal(price),
					fee = Decimal("0.00"),
					method = f"{net} - {purchase['data']['msg']}",
					trans_type = f"Data",
					credit = False,
					status = "success"
				)
				wallet.amount -= Decimal(price)
				wallet.bonus += Decimal(price)*Decimal(interest)
				wallet.save()
				ref_sys = ReferralSystem.objects.last()
				if ref_sys.status == True:
					my_refer = UserRef.objects.get(user=request.user)
					if my_refer.first_bonus == False:
						referral = my_refer.referred_by
						ref_wallet = Wallet.objects.get(user=referral)
						interest = ref_sys.referral_bonus/100
						bonus_point = interest*Decimal(price)
						ref_wallet.bonus += bonus_point
						ref_wallet.save()
						my_refer.first_bonus = True
						my_refer.save()
				return Response({"status": True, "message": purchase['data']['msg']}, status=status.HTTP_200_OK)
		except:
			return Response({"status": False, "message": "There was an error parsing your request. Please and try again."}, status=status.HTTP_417_EXPECTATION_FAILED)


class Airtime(APIView):
	
	def post(self, request):
		try:
			network = request.data.get("network")
			mobile_number = request.data.get("mobile_number")
			airtime_type = request.data.get("airtime_type")
			amount = request.data.get("amount")
			wallet = Wallet.objects.get(user=request.user)
			ref = f"{website.prefix}-{gen_key(8)}"
			if wallet.amount < Decimal(amount):
				return Response({"status": False, "message": "Insufficient funds. Please recharge and try again."}, status=status.HTTP_402_PAYMENT_REQUIRED)
			purchase = SME.purchaseAirtime(amount, network, mobile_number, ref)
			comm = AirtimeCommission.objects.last()
			if network == '1':
				if request.user.user_type == 'vendor':
					interest = comm.mtn_ven/100
				elif request.user.user_type == 'api':
					interest = comm.mtn_api/100
				else:
					interest = 0
				net = 'MTN'
			elif network == '2':
				if request.user.user_type == 'vendor':
					interest = comm.airtel_ven/100
				elif request.user.user_type == 'api':
					interest = comm.airtel_api/100
				else:
					interest = 0
				net = 'Airtel'
			elif network == '3':
				if request.user.user_type == 'vendor':
					interest = comm.etisalat_ven/100
				elif request.user.user_type == 'api':
					interest = comm.etisalat_api/100
				else:
					interest = 0
				net = '9mobile'
			elif network == '4':
				if request.user.user_type == 'vendor':
					interest = comm.glo_ven/100
				elif request.user.user_type == 'api':
					interest = comm.glo_api/100
				else:
					interest = 0
				net = 'Glo'
			
			if purchase['status'] == False:
				if "wallet" in purchase['msg']:
					return Response({"status": False, "message": "There was an error purchasing your airtime plan. Please try again later."}, status=status.HTTP_400_BAD_REQUEST)
				elif "Insufficient" in purchase["msg"]:
					DOJAH_API.SendSMS(website.whatsapp_number, purchase["msg"])
					DOJAH_API.SendWhatsApp(website.whatsapp_number, purchase["msg"])
					return Response({"status": False, "message": "There was an error purchasing your data plan. Report to the Administrator"}, status=status.HTTP_400_BAD_REQUEST)
				elif "license" in purchase["msg"]:
					DOJAH_API.SendSMS(website.whatsapp_number, f"{purchase['msg']} - SMEPlug")
					DOJAH_API.SendWhatsApp(website.whatsapp_number, f"{purchase['msg']} - SMEPlug")
					return Response({"status": False, "message": "An unknown error occurred. Please contact the Administrator."}, status=status.HTTP_400_BAD_REQUEST)
				else:
					return Response({"status": False, "message": purchase['msg']}, status=status.HTTP_400_BAD_REQUEST)
			else:
				Transaction.objects.create(
					user=request.user,
					reference = purchase['data']['reference'],
					ps_ref = ref,
					amount = Decimal(amount),
					fee = Decimal("0.00"),
					method = f"{net} - {purchase['data']['msg']}",
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
					if my_refer.first_bonus == False:
						referral = my_refer.referred_by
						ref_wallet = Wallet.objects.get(user=referral)
						interest = ref_sys.referral_bonus/100
						bonus_point = interest*Decimal(amount)
						ref_wallet.bonus += bonus_point
						ref_wallet.save()
						my_refer.first_bonus = True
						my_refer.save()
				return Response({"status": True, "message": purchase['data']['msg']}, status=status.HTTP_200_OK)
		except:
			return Response({"status": False, "message": "There was an error parsing your request. Please and try again."}, status=status.HTTP_417_EXPECTATION_FAILED)


class BillsPayment(APIView):
	def post(self, request):
		try:
			disco_name = request.data.get("disco_name")
			meter_number = request.data.get("meter_number")
			meter_type = request.data.get("meter_type")
			amount = request.data.get("amount")
			phone = request.data.get("phone")
			wallet = Wallet.objects.get(user=request.user)
			ref = f"{datetime.today().strftime('%Y%m%d%H%M')}{website.prefix}"
			if wallet.amount < Decimal(amount):
				return Response({"status": False, "message": "Insufficient funds. Please recharge and try again."}, status=status.HTTP_402_PAYMENT_REQUIRED)
			purchase = VTPass.PurchaseDisco(disco_name, meter_type, meter_number, phone, amount, ref)
			comm = BillsCommission.objects.last()
			if request.user.user_type == 'vendor':
				interest = comm.edc_ven/100
			elif request.user.user_type == 'api':
				interest = comm.edc_api/100
			else:
				interest = 0
			if purchase['response_description'] == 'TRANSACTION SUCCESSFUL':
				Transaction.objects.create(
					user=request.user,
					reference = purchase['data']['reference'],
					ps_ref = ref,
					amount = Decimal(amount),
					fee = Decimal("0.00"),
					method = f"{disco_name.upper()} - {purchase['data']['msg']}",
					trans_type = f"Electricity",
					credit = False,
					status = "success"
				)
				wallet.amount -= Decimal(amount)
				wallet.bonus += Decimal(amount)*Decimal(interest)
				wallet.save()
				ref_sys = ReferralSystem.objects.last()
				if ref_sys.status == True:
					my_refer = UserRef.objects.get(user=request.user)
					if my_refer.first_bonus == False:
						referral = my_refer.referred_by
						ref_wallet = Wallet.objects.get(user=referral)
						interest = ref_sys.referral_bonus/100
						bonus_point = interest*Decimal(amount)
						ref_wallet.bonus += bonus_point
						ref_wallet.save()
						my_refer.first_bonus = True
						my_refer.save()
				return Response({"status": True, "message": purchase['data']['msg']}, status=status.HTTP_200_OK)
			elif 'LOW' in purchase['response_description']:
				DOJAH_API.SendSMS(website.whatsapp_number, f"{purchase['response_description']} from VTPass")
				DOJAH_API.SendWhatsApp(website.whatsapp_number, f"{purchase['response_description']} from VTPass")
				return Response({"status": False, "message": "There was an error purchasing your data plan. Report to the Administrator"}, status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response({"status": False, "message": purchase['response_description']}, status=status.HTTP_400_BAD_REQUEST)
		except:
			return Response({"status": False, "message": "There was an error parsing your request. Please and try again."}, status=status.HTTP_417_EXPECTATION_FAILED)


class CablePayment(APIView):
	def get(self, request, decoder=None):
		try:
			user = request.user
			if user.user_type == 'reseller':
				plans = CablePlan.objects.filter(decoder__slug=decoder, active=True).values('pid', 'decoder', 'plan', 'reseller_user_price')
			else:
				plans = CablePlan.objects.filter(decoder__slug=decoder, active=True).values('pid', 'decoder', 'plan', 'customer_price')
			
			dataPlan = []
			for p in plans:
				dataPlans = {
					"id": p['pid'],
					"decoder": decoder,
					"plan": p['plan'],
					'amount': p['reseller_user_price'] if user.user_type == 'reseller' else p['customer_price']
				}
				dataPlan.append(dataPlans)
			return Response({"status": True, "message": "Data Queried Successfully", "data": dataPlan}, status=status.HTTP_200_OK)
		except:
			return Response({"status": False, "message": "There was an error parsing your request. Please and try again."}, status=status.HTTP_417_EXPECTATION_FAILED)
	
	def post(self, request):
		try:
			cable_name = request.data.get("decoder")
			variation_code = request.data.get("variation_code")
			iuc = request.data.get("smart_card_number")
			amount = request.data.get("amount")
			phone = request.data.get("phone")
			wallet = Wallet.objects.get(user=request.user)
			ref = f"{datetime.today().strftime('%Y%m%d%H%M')}{website.prefix}"
			if wallet.amount < Decimal(amount):
				return Response({"status": False, "message": "Insufficient funds. Please recharge and try again."}, status=status.HTTP_402_PAYMENT_REQUIRED)
			purchase = VTPass.PurchaseTV(cable_name, iuc, variation_code, phone, ref)
			if purchase['response_description'] == 'TRANSACTION SUCCESSFUL':
				Transaction.objects.create(
					user=request.user,
					reference = purchase['data']['reference'],
					ps_ref = ref,
					amount = Decimal(amount),
					fee = Decimal("0.00"),
					method = f"{cable_name.upper()} - {purchase['data']['msg']}",
					trans_type = f"Cable TV",
					credit = False,
					status = "success"
				)
				wallet.amount -= Decimal(amount)
				wallet.save()
				ref_sys = ReferralSystem.objects.last()
				if ref_sys.status == True:
					my_refer = UserRef.objects.get(user=request.user)
					if my_refer.first_bonus == False:
						referral = my_refer.referred_by
						ref_wallet = Wallet.objects.get(user=referral)
						interest = ref_sys.referral_bonus/100
						bonus_point = interest*Decimal(amount)
						ref_wallet.bonus += bonus_point
						ref_wallet.save()
						my_refer.first_bonus = True
						my_refer.save()
				return Response({"status": True, "message": purchase['data']['msg']}, status=status.HTTP_200_OK)
			elif 'LOW' in purchase['response_description']:
				DOJAH_API.SendSMS(website.whatsapp_number, f"{purchase['response_description']} from VTPass")
				DOJAH_API.SendWhatsApp(website.whatsapp_number, f"{purchase['response_description']} from VTPass")
				return Response({"status": False, "message": "There was an error purchasing your data plan. Report to the Administrator"}, status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response({"status": False, "message": purchase['response_description']}, status=status.HTTP_400_BAD_REQUEST)
		except:
			return Response({"status": False, "message": "There was an error parsing your request. Please and try again."}, status=status.HTTP_417_EXPECTATION_FAILED)


class ValidateIUCMeter(APIView):
	def get(self, request, val=None):
		if val == "iuc":
			try:
				decoder = request.GET.get("decoder")
				iuc = request.GET.get("smart_card_number")
				query = VTPass.ValidateIUC(decoder.lower(), iuc)
				if 'error' in query['content']:
					return Response({"status": False, "message": query['content']['error']}, status=status.HTTP_400_BAD_REQUEST)
				else:
					return Response({"status": True, "message": "Successfully queried", "data": query['content']}, status=status.HTTP_200_OK)
			except:
				return Response({"status": False, "message": "There was an error parsing your request."}, status=status.HTTP_417_EXPECTATION_FAILED)
		elif val == "meter":
			try:
				disco_name = request.GET.get("disco_name")
				meter_number = request.GET.get("meter_number")
				meter_type = request.GET.get("meter_type")
				query = VTPass.ValidateDisco(disco_name, meter_type, meter_number)
				if 'errors' in query['content']:
					return Response({"status": False, "message": query['response_description']}, status=status.HTTP_400_BAD_REQUEST)
				else:
					return Response({"status": True, "message": "Successfully queried", "data": query['content']}, status=status.HTTP_200_OK)
			except:
				return Response({"status": False, "message": "There was an error parsing your request."}, status=status.HTTP_417_EXPECTATION_FAILED)
