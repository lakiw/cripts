from django.conf.urls import url

urlpatterns = [
    url(r'^add/$', 'add_email_address', prefix='cripts.email_addresses.views'),
    url(r'^list/$', 'email_addresses_listing', prefix='cripts.email_addresses.views'),
    url(r'^list/(?P<option>\S+)/$', 'email_addresses_listing', prefix='cripts.email_addresses.views'),
    url(r'^details/(?P<address>\S+)/$', 'email_address_detail', prefix='cripts.email_addresses.views'),
    url(r'^bulkadd/$', 'bulk_add_email_addresses', prefix='cripts.email_addresses.views'),
]
