from django.conf.urls import url

urlpatterns = [
    url(r'^list/$', 'hashes_listing', prefix='cripts.hashes.views'),
    url(r'^list/(?P<option>\S+)/$', 'hashes_listing', prefix='cripts.hashes.views'),
]
