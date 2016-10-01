import imp
import os

from django.conf import settings
from django.conf.urls import include, url

urlpatterns = [

    url(r'^', include('cripts.core.urls')),                        # Core
    url(r'^dashboards/', include('cripts.dashboards.urls')),       # Dashboard
    url(r'^comments/', include('cripts.comments.urls')),           # Commentss
    url(r'^events/', include('cripts.events.urls')),               # Events
    url(r'^notifications/', include('cripts.notifications.urls')), # Notifications
    url(r'^objects/', include('cripts.objects.urls')),             # Objects
    url(r'^relationships/', include('cripts.relationships.urls')), # Relationships
    url(r'^services/', include('cripts.services.urls')),           # Services
    url(r'^datasets/', include('cripts.datasets.urls')),           # Datasets
    url(r'^email_addresses/', include('cripts.email_addresses.urls')),  # Email Addresses
    url(r'^hashes/', include('cripts.hashes.urls')),               # Hashes
    url(r'^targets/', include('cripts.targets.urls')),             # Targets
    url(r'^usernames/', include('cripts.usernames.urls')),         # Services
]

# Error overrides
handler500 = 'cripts.core.errors.custom_500'
handler404 = 'cripts.core.errors.custom_404'
handler403 = 'cripts.core.errors.custom_403'
handler400 = 'cripts.core.errors.custom_400'

# Enable the API if configured
if settings.ENABLE_API:
    from tastypie.api import Api
    from cripts.comments.api import CommentResource
    from cripts.events.api import EventResource
    from cripts.services.api import ServiceResource
    from cripts.vocabulary.api import VocabResource

    v1_api = Api(api_name='v1')
    v1_api.register(CommentResource())
    v1_api.register(EventResource())
    v1_api.register(ServiceResource())
    v1_api.register(SignatureResource())
    v1_api.register(VocabResource())

    for service_directory in settings.SERVICE_DIRS:
        if os.path.isdir(service_directory):
            for d in os.listdir(service_directory):
                abs_path = os.path.join(service_directory, d, 'urls.py')
                if os.path.isfile(abs_path):
                    try:
                        rdef = imp.load_source('urls', abs_path)
                        rdef.register_api(v1_api)
                    except Exception, e:
                        pass

    urlpatterns.append(url(r'^api/', include(v1_api.urls)))

# This code allows static content to be served up by the development server
if settings.DEVEL_INSTANCE:
    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns.append(
            url(r'^%s(?P<path>.*)$' % _media_url, serve, {'document_root': settings.MEDIA_ROOT}))
    del(_media_url, serve)
