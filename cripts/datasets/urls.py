from django.conf.urls import url

urlpatterns = [
    url(r'^list/$', 'datasets_listing', prefix='cripts.datasets.views'),
    url(r'^list/(?P<option>\S+)/$', 'datasets_listing', prefix='cripts.datasets.views'),
    url(r'^upload/$', 'upload_dataset', prefix='cripts.datasets.views'),
]
