from django.conf.urls import url

urlpatterns = [
    url(r'^forge/$', 'add_new_relationship', prefix='cripts.relationships.views'),
    url(r'^breakup/$', 'break_relationship', prefix='cripts.relationships.views'),
    url(r'^get_dropdown/$', 'get_relationship_type_dropdown', prefix='cripts.relationships.views'),
    url(r'^update_relationship_confidence/$', 'update_relationship_confidence', prefix='cripts.relationships.views'),
    url(r'^update_relationship_reason/$', 'update_relationship_reason', prefix='cripts.relationships.views'),
    url(r'^update_relationship_type/$', 'update_relationship_type', prefix='cripts.relationships.views'),
    url(r'^update_relationship_date/$', 'update_relationship_date', prefix='cripts.relationships.views'),
]
