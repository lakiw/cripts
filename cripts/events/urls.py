from django.conf.urls import url

urlpatterns = [
    url(r'^details/(?P<eventid>\w+)/$', 'view_event', prefix='cripts.events.views'),
    url(r'^add/$', 'add_event', prefix='cripts.events.views'),
    url(r'^search/$', 'event_search', prefix='cripts.events.views'),
    url(r'^remove/(?P<_id>[\S ]+)$', 'remove_event', prefix='cripts.events.views'),
    url(r'^set_title/(?P<event_id>\w+)/$', 'set_event_title', prefix='cripts.events.views'),
    url(r'^set_type/(?P<event_id>\w+)/$', 'set_event_type', prefix='cripts.events.views'),
    url(r'^get_event_types/$', 'get_event_type_dropdown', prefix='cripts.events.views'),
    url(r'^list/$', 'events_listing', prefix='cripts.events.views'),
    url(r'^list/(?P<option>\S+)/$', 'events_listing', prefix='cripts.events.views'),
]
