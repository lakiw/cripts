from django.conf.urls import url

urlpatterns = [
    url(r'^list/$', 'usernames_listing', prefix='cripts.usernames.views'),
    url(r'^list/(?P<option>\S+)/$', 'usernames_listing', prefix='cripts.usernames.views'),
]
