from django.urls import re_path as _

from backbone.views import A2CSettings, APISettings, APIUsers, AddAdmin, AddContact, AdminUsers, AirtimeReq, AirtimeSettings,\
    AllECards, AllECards9mobile, AllECardsAirtel, AllECardsGlo, AllEPins, AllEPinsNeco, Announcements, BillsSettings, CablePlug,\
    Contacts, DataPlug, DataSettings, DelAnn, DelContact, DelECard, DelEPin, DelReq, DelStaff, DelTransaction, DelUser, DelWTransaction,\
    ECards, EPinSettings, EPins, Home, Login, LogoSettings, Logout, DeleteUsedCard, NetworkSet, ProductSettings, ReferralSettings, Resellers,\
    SEOSettings, TransactionDetail, Transactions, UserProfile, Users, WalletTransaction, WalletTransactions, Webhook, WebsiteDetails,\
    fetchCablePlug, DeleteData, fetchDataPlug, myProfile, updateUserWallet

urlpatterns = [
    _(r'^$', Home, name="a_home"),
    _(r'^login\/?$', Login, name="a_login"),
    _(r'^logout\/?$', Logout, name="a_logout"),
    _(r'^profile\/?$', myProfile, name="a_profile"),
    
    _(r'^transactionList\/?$', Transactions, name="a_transactions"),
    _(r'^transactionView/(?P<ref>[\w-]+)/$', TransactionDetail, name="a_transactions_det"),
    _(r'^transactionRemove/(?P<ref>[\w-]+)/$', DelTransaction, name="a_transactions_del"),
    _(r'^walletHistory\/?$', WalletTransactions, name="a_wallettransactions"),
    _(r'^walletHistoryView/(?P<ref>[\w-]+)/$', WalletTransaction, name="a_wallettransactions_det"),
    _(r'^walletHistoryRemove/(?P<ref>[\w-]+)/$', DelWTransaction, name="a_wallet_del"),
    _(r'^staffs/$', AdminUsers, name="a_admins"),
    _(r'^staffs/add/$', AddAdmin, name="a_new_staff"),
    _(r'^staff/delete/(?P<username>[\w-]+)/$', DelStaff, name="a_del_staff"),
    _(r'^customers/$', Users, name="a_users"),
    _(r'^user/delete/(?P<username>[\w-]+)/$', DelUser, name="a_users_del"),
    _(r'^resellers/$', Resellers, name="a_res_users"),
    _(r'^api_userss/$', APIUsers, name="a_api_users"),
    _(r'^user/update/(?P<username>[\w-]+)/$', UserProfile, name="a_user_update"),
    _(r'^wallet/update/(?P<username>[\w-]+)/$', updateUserWallet, name="a_wallet_update"),
    _(r'^contacts/$', Contacts, name="a_contacts"),
    _(r'^contact/new/$', AddContact, name="a_contact"),
    _(r'^contact/delete/(?P<pk>[\w-]+)/$', DelContact, name="a_del_contact"),

    # Configuration
    _(r'^website-settings\/?$', WebsiteDetails, name="web_set"),
    _(r'^webhook-settings\/?$', Webhook, name="webhook_set"),
    _(r'^website-logo\/?$', LogoSettings, name="logo_set"),
    _(r'^api-settings\/?$', APISettings, name="api_set"),
    _(r'^a2c-settings\/?$', A2CSettings, name="a2c_set"),
    _(r'^referral-settings\/?$', ReferralSettings, name="ref_set"),
    _(r'^data-settings\/?$', DataSettings, name="data_set"),
    _(r'^airtime-settings\/?$', AirtimeSettings, name="airtime_set"),
    _(r'^bills-settings\/?$', BillsSettings, name="bills_set"),
    _(r'^seo-settings\/?$', SEOSettings, name="seo_set"),
    _(r'^e-airtime-settings\/?$', ECards, name="e_card_set"),
    _(r'^e-airtimes\/?$', AllECards, name="a_ecard"),
    _(r'^e-airtimes_glo\/?$', AllECardsGlo, name="a_ecard_glo"),
    _(r'^e-airtimes_airtel\/?$', AllECardsAirtel, name="a_ecard_airtel"),
    _(r'^e-airtimes_9mobile\/?$', AllECards9mobile, name="a_ecard_9mobile"),
    _(r'^e-airtime/(?P<pk>[\w-]+)/$', DelECard, name="a_ecard_del"),
    _(r'^e-pin-settings\/?$', EPins, name="e_pin_set"),
    _(r'^epins/$', AllEPins, name="a_epin"),
    _(r'^epins_neco/$', AllEPinsNeco, name="a_epin_neco"),
    _(r'^e-pin/(?P<pk>[\w-]+)/$', DelEPin, name="a_epin_del"),
    _(r'^card-settings\/?$', EPinSettings, name="pin_settings"),
    _(r'^card-delete\/?$', DeleteUsedCard, name="pin_delete"),
    _(r'^announcement-delete/(?P<pk>[\w-]+)\/?$', DelAnn, name="a_ann_del"),
    _(r'^announcements\/?$', Announcements, name="a_ann"),
    _(r'^airtime-req-delete/(?P<pk>[\w-]+)\/?$', DelReq, name="a_req_del"),
    _(r'^airtime-requests\/?$', AirtimeReq, name="a_req"),
    
    # Products
    _(r'^networks\/?$', NetworkSet, name="a_networks"),
    _(r'^dataplans/(?P<net>[\w-]+)\/?$', DataPlug, name="a_data_plans"),
    _(r'^delete-plans/(?P<net>[\w-]+)/(?P<pid>[\w-]+)\/?$', DeleteData, name="a_data_plans_del"),
    _(r'^fetchplans/(?P<net>[\w-]+)\/?$', fetchDataPlug, name="a_data_plans_fetch"),

    _(r'^cableplugs/(?P<decoder>[\w-]+)\/?$', CablePlug, name="a_cables"),
    _(r'^fetchcable/(?P<decoder>[\w-]+)\/?$', fetchCablePlug, name="a_cable_fetch"),

    # Product Settings
    _(r'^product-settings\/?$', ProductSettings, name="product_set"),
]