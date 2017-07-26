from django.conf.urls import url

urlpatterns = [
    url(r'^remove/(?P<obj_type>\S+)/(?P<obj_id>\S+)/$', 'remove_comment', prefix='cripts.comments.views'),
    url(r'^(?P<method>\S+)/(?P<obj_type>\S+)/(?P<obj_id>\S+)/$', 'add_update_comment', prefix='cripts.comments.views'),
    url(r'^activity/$', 'activity', prefix='cripts.comments.views'),
    url(r'^activity/(?P<atype>\S+)/(?P<value>\S+)/$', 'activity', prefix='cripts.comments.views'),
    url(r'^activity/get_new_comments/$', 'get_new_comments', prefix='cripts.comments.views'),
    url(r'^search/(?P<stype>[A-Za-z0-9\-\._]+)/(?P<sterm>.+?)/$', 'comment_search', prefix='cripts.comments.views'),
    url(r'^list/$', 'comments_listing', prefix='cripts.comments.views'),
    url(r'^list/(?P<option>\S+)/$', 'comments_listing', prefix='cripts.comments.views'),
]
