from mongoengine import Document, StringField, UUIDField, ListField
from django.conf import settings

from cripts.core.cripts_mongoengine import CriptsBaseAttributes, CriptsSourceDocument
from cripts.core.cripts_mongoengine import CriptsActionsDocument


class HashStats(CriptsBaseAttributes, CriptsSourceDocument, CriptsActionsDocument,
            Document):
    """
    HashStats class.
    """

    meta = {
        "collection": settings.COL_HASH_STATS,
        "cripts_type": 'HashStats',
        "latest_schema_version": 1,
        "schema_doc": {
            'display_name': 'Display name to show the user, aka "Raw MD5"',
            'hash_name': 'The internal name to reference the hash type',
        },
        "jtable_opts": {
                         'details_url': 'cripts.hash_types.views.hash_stat_detail',
                         'details_url_key': "hash_name",
                         'default_sort': "display_name",
                         'fields': [ "display_name"],
                         'jtopts_fields': [ "display_name"],
                         'hidden_fields': [],
                         'linked_fields': [ ],
                         'details_link': "display_name",
                         'no_sort': []
                       }

    }
    display_name = StringField(required=True)
    hash_name = StringField(required=True)
  
