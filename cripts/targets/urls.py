from django.conf.urls import url

urlpatterns = [
    url(r'^list/$', 'targets_listing', prefix='cripts.targets.views'),
    url(r'^list/(?P<option>\S+)/$', 'targets_listing', prefix='cripts.targets.views'),
]
