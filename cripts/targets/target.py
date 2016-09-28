import uuid

from mongoengine import Document, StringField, UUIDField
from django.conf import settings

from cripts.core.cripts_mongoengine import CriptsBaseAttributes, CriptsSourceDocument
from cripts.core.cripts_mongoengine import CriptsActionsDocument


class Target(CriptsBaseAttributes, CriptsSourceDocument, CriptsActionsDocument,
            Document):
    """
    Target class.
    """

    meta = {
        "collection": settings.COL_HASHES,
        "cripts_type": 'Target',
        "latest_schema_version": 1,
        "schema_doc": {
            'type': 'If the target is a person, service, or server',
            'source': ('List [] of sources who provided information about this'
                ' target')
        },
        "jtable_opts": {
                         'details_url': 'cripts.targets.views.view_target',
                         'details_url_key': 'id',
                         'default_sort': "created DESC",
                         'searchurl': 'cripts.targets.views.targets_listing',
                         'fields': [ "created",
                                     "source", "id"],
                         'jtopts_fields': [
                                            "created",
                                            "source",
                                            "favorite",
                                            "id"],
                         'hidden_fields': [],
                         'linked_fields': ["source", ],
                         'details_link': 'details',
                         'no_sort': ['details']
                       }

    }

    
