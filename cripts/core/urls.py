from django.conf.urls import url
from django.contrib.auth.views import logout_then_login

urlpatterns = [

    # Authentication
    url(r'^login/$', 'cripts.core.views.login'),
    url(r'^logout/$', logout_then_login),

    # Buckets
    url(r'^bucket/list/$', 'cripts.core.views.bucket_list'),
    url(r'^bucket/list/(?P<option>.+)$', 'cripts.core.views.bucket_list'),
    url(r'^bucket/mod/$', 'cripts.core.views.bucket_modify'),
    url(r'^bucket/autocomplete/$', 'cripts.core.views.bucket_autocomplete'),
    url(r'^bucket/promote/$', 'cripts.core.views.bucket_promote'),

    # Common functionality for all TLOs
    url(r'^status/update/(?P<type_>\S+)/(?P<id_>\S+)/$', 'cripts.core.views.update_status'),
    url(r'^search/$', 'cripts.core.views.global_search_listing'),
    url(r'^object/download/$', 'cripts.core.views.download_object'),
    url(r'^files/download/(?P<sample_md5>\w+)/$', 'cripts.core.views.download_file'),
    url(r'^object/sources/removeall/(?P<obj_type>\S+)/(?P<obj_id>\S+)/$', 'cripts.core.views.remove_all_source'),
    url(r'^object/sources/remove/(?P<obj_type>\S+)/(?P<obj_id>\S+)/$', 'cripts.core.views.remove_source'),
    url(r'^object/sources/(?P<method>\S+)/(?P<obj_type>\S+)/(?P<obj_id>\S+)/$', 'cripts.core.views.add_update_source'),
    url(r'^source_releasability/$', 'cripts.core.views.source_releasability'),
    url(r'^tickets/(?P<method>\S+)/(?P<type_>\w+)/(?P<id_>\w+)/$', 'cripts.core.views.add_update_ticket'),
    url(r'^preferred_actions/$', 'cripts.core.views.add_preferred_actions'),
    url(r'^actions/(?P<method>\S+)/(?P<obj_type>\S+)/(?P<obj_id>\w+)/$', 'cripts.core.views.add_update_action'),
    url(r'^action/remove/(?P<obj_type>\S+)/(?P<obj_id>\w+)/$', 'cripts.core.views.remove_action'),
    url(r'^add_action/$', 'cripts.core.views.new_action'),
    url(r'^get_actions_for_tlo/$', 'cripts.core.views.get_actions_for_tlo'),


    # cripts Configuration
    url(r'^config/$', 'cripts.config.views.cripts_config'),
    url(r'^modify_config/$', 'cripts.config.views.modify_config'),
    url(r'^audit/list/$', 'cripts.core.views.audit_listing'),
    url(r'^audit/list/(?P<option>\S+)/$', 'cripts.core.views.audit_listing'),
    url(r'^items/editor/$', 'cripts.core.views.item_editor'),
    url(r'^items/list/$', 'cripts.core.views.items_listing'),
    url(r'^items/list/(?P<itype>\S+)/(?P<option>\S+)/$', 'cripts.core.views.items_listing'),
    url(r'^items/toggle_active/$', 'cripts.core.views.toggle_item_active'),
    url(r'^users/toggle_active/$', 'cripts.core.views.toggle_user_active'),
    url(r'^users/list/$', 'cripts.core.views.users_listing'),
    url(r'^users/list/(?P<option>\S+)/$', 'cripts.core.views.users_listing'),
    url(r'^get_item_data/$', 'cripts.core.views.get_item_data'),
    url(r'^add_action/$', 'cripts.core.views.new_action'),

    # Default landing page
    url(r'^$', 'cripts.dashboards.views.dashboard'),
    url(r'^counts/list/$', 'cripts.core.views.counts_listing'),
    url(r'^counts/list/(?P<option>\S+)/$', 'cripts.core.views.counts_listing'),

    # Dialogs
    url(r'^get_dialog/(?P<dialog>[A-Za-z0-9\-\._-]+)$', 'cripts.core.views.get_dialog'),
    url(r'^get_dialog/$', 'cripts.core.views.get_dialog'),

    # General core pages
    url(r'^details/(?P<type_>\S+)/(?P<id_>\S+)/$', 'cripts.core.views.details'),
    url(r'^update_object_description/', 'cripts.core.views.update_object_description'),
    url(r'^update_object_data/', 'cripts.core.views.update_object_data'),

    # Helper pages
    url(r'^about/$', 'cripts.core.views.about'),
    url(r'^help/$', 'cripts.core.views.help'),
    url(r'^get_search_help/$', 'cripts.core.views.get_search_help'),

    # Sectors
    url(r'^sector/list/$', 'cripts.core.views.sector_list'),
    url(r'^sector/list/(?P<option>.+)$', 'cripts.core.views.sector_list'),
    url(r'^sector/mod/$', 'cripts.core.views.sector_modify'),
    url(r'^sector/options/$', 'cripts.core.views.get_available_sectors'),

    # Timeline
    url(r'^timeline/(?P<data_type>\S+)/$', 'cripts.core.views.timeline'),
    url(r'^timeline/(?P<data_type>\S+)/(?P<extra_data>\S+)/$', 'cripts.core.views.timeline'),
    url(r'^timeline/$', 'cripts.core.views.timeline'),

    # User Stuff
    url(r'^profile/(?P<user>\S+)/$', 'cripts.core.views.profile'),
    url(r'^profile/$', 'cripts.core.views.profile'),
    url(r'^source_access/$', 'cripts.core.views.source_access'),
    url(r'^source_add/$', 'cripts.core.views.source_add'),
    url(r'^get_user_source_list/$', 'cripts.core.views.get_user_source_list'),
    url(r'^user_role_add/$', 'cripts.core.views.user_role_add'),
    url(r'^user_source_access/$', 'cripts.core.views.user_source_access'),
    url(r'^user_source_access/(?P<username>\S+)/$', 'cripts.core.views.user_source_access'),
    url(r'^preference_toggle/(?P<section>\S+)/(?P<setting>\S+)/$', 'cripts.core.views.user_preference_toggle'),
    url(r'^preference_update/(?P<section>\S+)/$', 'cripts.core.views.user_preference_update'),
    url(r'^clear_user_notifications/$', 'cripts.core.views.clear_user_notifications'),
    url(r'^delete_user_notification/(?P<type_>\S+)/(?P<oid>\S+)/$', 'cripts.core.views.delete_user_notification'),
    url(r'^change_subscription/(?P<stype>\S+)/(?P<oid>\S+)/$', 'cripts.core.views.change_subscription'),
    url(r'^source_subscription/$', 'cripts.core.views.source_subscription'),
    url(r'^change_password/$', 'cripts.core.views.change_password'),
    url(r'^change_totp_pin/$', 'cripts.core.views.change_totp_pin'),
    url(r'^reset_password/$', 'cripts.core.views.reset_password'),
    url(r'^favorites/toggle/$', 'cripts.core.views.toggle_favorite'),
    url(r'^favorites/view/$', 'cripts.core.views.favorites'),
    url(r'^favorites/list/(?P<ctype>\S+)/(?P<option>\S+)/$', 'cripts.core.views.favorites_list'),

    # User API Authentication
    url(r'^get_api_key/$', 'cripts.core.views.get_api_key'),
    url(r'^create_api_key/$', 'cripts.core.views.create_api_key'),
    url(r'^make_default_api_key/$', 'cripts.core.views.make_default_api_key'),
    url(r'^revoke_api_key/$', 'cripts.core.views.revoke_api_key'),

]
