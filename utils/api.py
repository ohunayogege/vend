from django.conf import settings
import requests, json, base64
from requests.auth import HTTPBasicAuth
from backbone.models import APISetting

api = APISetting.objects.last()
sme_web = settings.SME_LINK
sme_api = settings.SME_API
def getUserDetail():
	url = f"{sme_web}/extra/"
	headers = {
		"Authorization": f"Token {sme_api}",
		"Content-Type": "application/json"
	}
	x = requests.get(url, headers=headers)
	return x.json()


class DOJAH_API():
	key = getUserDetail()
	prod = "https://api.dojah.io"
	headers = {
		"AppId": key['data']['dojah']['app_key'],
		"Authorization": key['data']['dojah']['api_key']
	}

	# Send OTP
	def SendWhatsApp(mobile, message):
		url = f"{DOJAH_API.prod}/api/v1/messaging/sms"
		params = {
			"destination": mobile,
			"message": message,
			"channel": "whatsapp",
			"sender_id": "OTP Code",
			"priority": True
		}
		x = requests.post(url, headers=DOJAH_API.headers, data=params)
		return x.json()
	
	def SendSMS(mobile, message):
		url = f"{DOJAH_API.prod}/api/v1/messaging/sms"
		params = {
			"destination": mobile,
			"message": message,
			"channel": "sms",
			"sender_id": "OTP Code",
			"priority": True
		}
		x = requests.post(url, headers=DOJAH_API.headers, data=params)
		return x.json()
	
	def resolveNuban(account_number, bank_code):
		url = f"{DOJAH_API.prod}/api/v1/general/account"
		params = {
			"account_number": account_number,
			"bank_code": bank_code
		}
		x = requests.get(url, headers=DOJAH_API.headers, params=params)
		return x.json()


class Monnify():
	MonnifyAPI = api.monnify_api_key
	MonnifySecret = api.monnify_secret_key
	monnify = MonnifyAPI+":"+MonnifySecret
	message_bytes = monnify.encode('utf-8')
	MonnifyLogin = base64.b64encode(message_bytes)
	mon = str(MonnifyLogin).split("b")[1]
	mon2 = mon.rsplit("'")[1]

	link = "https://api.monnify.com/api/v2"
	sa = "https://sandbox.monnify.com/api/v2"
	log_link = "https://api.monnify.com/api/v1/auth/login"
	headers = {
		"Authorization": f"Bearer {mon2}",
		"Content-Type": "application/json"
	}

	def Login():
		url = Monnify.log_link
		headers = {
			"Authorization": f"Basic {Monnify.mon2}",
			"Content-Type": "application/json"
		}		
		x = requests.post(url=url, headers=headers)
		return x.json()

	def VirtualAccount(name, email, ref):
		url = f"{Monnify.link}/bank-transfer/reserved-accounts"
		logged = Monnify.Login()
		headers = {
			"Authorization": f"Bearer {logged['responseBody']['accessToken']}",
			"Content-Type": "application/json"
		}
		datum = {
			"accountReference": ref,
			"accountName": name,
			"currencyCode": "NGN",
			"contractCode": api.monnify_contract_code,
			"customerEmail": email,
			"customerName": name,
			"getAllAvailableBanks": True
		}
		x = requests.post(url=url, data=json.dumps(datum), headers=headers)
		return x.json()
	
	def VirtualAccountNew(name, email, bank, ref):
		url = f"{Monnify.link}/bank-transfer/reserved-accounts"
		logged = Monnify.Login()
		headers = {
			"Authorization": f"Bearer {logged['responseBody']['accessToken']}",
			"Content-Type": "application/json"
		}
		datum = {
			"accountReference": ref,
			"accountName": name,
			"currencyCode": "NGN",
			"contractCode": api.monnify_contract_code,
			"customerEmail": email,
			"customerName": name,
			"getAllAvailableBanks": False,
			"preferredBanks": [bank]
		}
		x = requests.post(url=url, data=json.dumps(datum), headers=headers)
		return x.json()
	
	def getBanks():
		url = f"https://api.monnify.com/api/v1/banks"
		logged = Monnify.Login()
		headers = {
			"Authorization": f"Bearer {logged['responseBody']['accessToken']}",
			"Content-Type": "application/json"
		}
		x = requests.get(url=url, headers=headers)
		return x.json()


def TVBills(decoder):
	url = f"{sme_web}/cablesub/{decoder}"
	header = {
		"Content-Type": "application/json",
		"Authorization": f"Token {sme_api}"
	}
	x = requests.get(url=url, headers=header)
	return x.json()

def ValidateIUC(decoder, iuc):
	url = f"{sme_web}/validate/iuc/"
	header = {
		"Content-Type": "application/json",
		"Authorization": f"Token {sme_api}"
	}
	datum = {
		"smart_card_number": iuc,
		"decoder": decoder
	}
	x = requests.get(url=url, headers=header, params=datum)
	return x.json()

def PurchaseTV(decoder, iuc, variation_code, phone, amount, ref):
	url = f"{sme_web}/cablesub/"
	header = {
		"Content-Type": "application/json",
		"Authorization": f"Token {sme_api}"
	}
	datum = {
		"ref": ref,
		"smart_card_number": iuc,
		"decoder": decoder,
		"variation_code": variation_code,
		"amount": amount,
		"phone": phone
	}
	x = requests.post(url=url, headers=header, data=json.dumps(datum))
	return x.json()


def ValidateDisco(disco, disco_type, iuc):
	url = f"{sme_web}/validate/meter/"
	header = {
		"Content-Type": "application/json",
		"Authorization": f"Token {sme_api}"
	}
	datum = {
		"meter_number": iuc,
		"disco_name": disco,
		"meter_type": disco_type
	}
	x = requests.get(url=url, headers=header, params=datum)
	return x.json()

def PurchaseDisco(disco, disco_type, iuc, phone, amount, ref):
	url = f"{sme_web}/billpayment/"
	header = {
		"Content-Type": "application/json",
		"Authorization": f"Token {sme_api}"
	}
	datum = {
		"meter_number": iuc,
		"disco_name": disco,
		"meter_type": disco_type,
		"amount": amount,
		"phone": phone
	}
	x = requests.post(url=url, headers=header, data=json.dumps(datum))
	return x.json()

def SmilePlan():
	url = f"{sme_web}/service-variations?serviceID=smile-direct"
	header = {
		"Content-Type": "application/json",
		"Authorization": f"Token {sme_api}"
	}
	x = requests.get(url=url, headers=header)
	return x.json()

def PurchaseSmile(plan, phone, amount, ref):
	url = f"{sme_web}/pay"
	header = {
		"Content-Type": "application/json",
		"Authorization": f"Token {sme_api}"
	}
	datum = {
		"request_id": ref,
		"billersCode": phone,
		"serviceID": "smile-direct",
		"variation_code": plan,
		"amount": amount
	}
	x = requests.post(url=url, headers=header, params=datum)
	return x.json()

def ValidateSmile(phone):
	url = f"{sme_web}/merchant-verify/smile/phone"
	header = {
		"Content-Type": "application/json",
		"Authorization": f"Token {sme_api}"
	}
	datum = {
		"billersCode": phone,
		"serviceID": "smile-direct"
	}
	x = requests.post(url=url, headers=header, params=datum)
	return x.json()


def fetchPlans():
	url = f"{sme_web}/data/plans"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Token {sme_api}"
	}
	x = requests.get(url, headers=headers)
	return x.json()

def purchaseAirtime(amount, network, mobile, ref):
	url = f"{sme_web}/topup/"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Token {sme_api}"
	}
	datum = {
		"network": network,
		"amount": amount,
		"mobile_number": mobile,
		"customer_reference": ref,
		"airtime_type": "VTU"
	}
	x = requests.post(url, headers=headers, data=json.dumps(datum))
	return x.json()

def purchaseData(plan, network, mobile, ref):
	url = f"{sme_web}/data/"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Token {sme_api}"
	}
	datum = {
		"network": 1 if network == 'mtn' else 2 if network == 'airtel' else 3 if network == '9mobile' else 4,
		"plan": plan,
		"mobile_number": mobile
	}
	x = requests.post(url, headers=headers, data=json.dumps(datum))
	return x.json()

# def purchaseDataAPI(plan, network, mobile, ref):
# 	key = getUserDetail()
# 	url = "https://smeplug.ng/api/v1/data/purchase"
# 	headers = {
# 		"Content-Type": "application/json",
# 		"Authorization": f"Bearer {settings.SME_API}"
# 	}
# 	datum = {
# 		"network_id": network,
# 		"plan_id": plan,
# 		"phone": mobile
# 	}
# 	x = requests.post(url, headers=headers, data=json.dumps(datum))
# 	return x.json()
