from django.conf.urls import url

urlpatterns = [
    url(r'^add/$', 'add_username', prefix='cripts.usernames.views'),
    url(r'^list/$', 'usernames_listing', prefix='cripts.usernames.views'),
    url(r'^list/(?P<option>\S+)/$', 'usernames_listing', prefix='cripts.usernames.views'),
    url(r'^details/(?P<username_id>\S+)/$', 'username_detail', prefix='cripts.usernames.views'),
    url(r'^bulkadd/$', 'bulk_add_usernames', prefix='cripts.usernames.views'),
]
