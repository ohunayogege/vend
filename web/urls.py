from django.urls import re_path as _
from .views import AirtimeService, AirtimeToCash, BonusToWallet, Conts, DataService, DelMyCard, DelMyPin, DeveloperPage, FAQs, FetchCardDenomination, FetchNuban, ForgotPassword, FundWalletBank,\
    FundWalletCard, FundWalletCardValidate,\
    Home, Index, LoadPlans, Login, Logout, MetreBillsPayment, MonnifyWebhook, Notifications, Pricing, RechargeCardPrint, Register, ResetPassword,\
    ResultChecker, SMEPlugWebhook, SetPin, Setting, SmileNetwork, TVBillsPayment,\
    Transactions, UpdateBank, VTPassWebhook, VerifyAccount, ViewTransaction, Wallets, myCards, myEPins, myReferral, printAirtime


urlpatterns = [
    _(r'^$', Index, name="index"),
    # _(r'^<str:ref_code>\/?$', name='ref'),
    _(r'^home\/?$', Home, name="home"),
    _(r'^login\/?$', Login, name="login"),
    _(r'^logout', Logout, name="logout"),
    _(r'^register\/?$', Register, name="register"),
    _(r'^verify-account\/?$', VerifyAccount, name="verify_account"),
    _(r'^forgot-password\/?$', ForgotPassword, name="forgot_password"),
    _(r'^reset-password\/?$', ResetPassword, name="reset_password"),

    # Top Up Wallet
    _(r'^fund-wallet/bank\/?$', FundWalletBank, name='fund_bank'),
    _(r'^fund-wallet/card\/?$', FundWalletCard, name='fund_card'),
    _(r'^fund-wallet/confirm\/?$', FundWalletCardValidate, name='fund_card_confirm'),

    # Airtime and Data
    _(r'airtime\/?$', AirtimeService, name='airtime'),
    _(r'data\/?$', DataService, name='datas'),
    _(r'load_plans\/?$', LoadPlans, name='load_plans'),

    # Extras
    _(r'airtimeCash\/?$', AirtimeToCash, name='airtimeCash'),
    _(r'resultChecker\/?$', ResultChecker, name='resultChecker'),
    _(r'rechargePinOrder\/?$', RechargeCardPrint, name='card_print'),
    _(r'fetchRechargePinOrder\/?$', FetchCardDenomination, name='card_check'),
    _(r'bonus-wallet\/?$', BonusToWallet, name='bonusWallet'),

    # Bills
    _(r'^utilities/tv-subscription\/?$', TVBillsPayment, name="tv_decoder"),
    _(r'^utilities/meterToken\/?$', MetreBillsPayment, name="meter_token"),
    _(r'^utilities/smile-direct\/?$', SmileNetwork, name="smile-direct"),

    # Settings/Account
    _(r'^settings\/?$', Setting, name='settings'),
    _(r'^set_pin\/?$', SetPin, name='set_pin'),
    _(r'^fetchNuban\/?$', FetchNuban, name='fetch_nuban'),
    _(r'^updateBank\/?$', UpdateBank, name='updateBank'),
    _(r'^referral\/?$', myReferral, name='referral'),

    # Pricing
    _(r'pricing\/?$', Pricing, name='pricing'),
    _(r'our-contacts\/?$', Conts, name='contactList'),
    _(r'faqs\/?$', FAQs, name='faqs'),
    
    _(r'wallets\/?$', Wallets, name='wall'),
    _(r'gen-cards\/?$', myCards, name='cards'),
    _(r'gen-cards-rec/(?P<pk>[\w-]+)\/?$', printAirtime, name='print_cards'),
    _(r'del-card/(?P<pk>[\w-]+)\/?$', DelMyCard, name='del_card'),
    _(r'del-pin/(?P<pk>[\w-]+)\/?$', DelMyPin, name='del_pin'),
    _(r'e-pins\/?$', myEPins, name='epins'),
    _(r'notifications\/?$', Notifications, name='notif'),
    _(r'transactions\/?$', Transactions, name='trans'),
    _(r'transaction/(?P<ref>[\w-]+)\/?$', ViewTransaction, name='view_trans'),
    _(r'developers/\/?$', DeveloperPage, name='docs'),

    _(r'^webhook/monnify\/?$', MonnifyWebhook),
    _(r'^webhook/vtpass\/?$', VTPassWebhook),
    _(r'^webhook/sme\/?$', SMEPlugWebhook),
]
