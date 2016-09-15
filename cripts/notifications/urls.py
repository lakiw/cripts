from django.conf.urls import url

urlpatterns = [
    url(r'^poll/$', 'poll', prefix='cripts.notifications.views'),
    url(r'^ack/$', 'acknowledge', prefix='cripts.notifications.views'),
]
