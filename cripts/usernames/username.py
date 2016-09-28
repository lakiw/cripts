import uuid

from mongoengine import Document, StringField, UUIDField
from django.conf import settings

from cripts.core.cripts_mongoengine import CriptsBaseAttributes, CriptsSourceDocument
from cripts.core.cripts_mongoengine import CriptsActionsDocument


class UserName(CriptsBaseAttributes, CriptsSourceDocument, CriptsActionsDocument,
            Document):
    """
    UserName class.
    """

    meta = {
        "collection": settings.COL_USERNAMES,
        "cripts_type": 'UserName',
        "latest_schema_version": 1,
        "schema_doc": {
            'username': 'The actual username',
            'source': ('List [] of sources who provided information about this'
                ' username')
        },
        "jtable_opts": {
                         'details_url': 'cripts.usernames.views.view_username',
                         'details_url_key': 'id',
                         'default_sort': "created DESC",
                         'searchurl': 'cripts.usernames.views.usernames_listing',
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

    
