import uuid

from mongoengine import Document, StringField, UUIDField
from mongoengine import BooleanField, EmbeddedDocument
from django.conf import settings

from cripts.core.cripts_mongoengine import CriptsBaseAttributes, CriptsSourceDocument
from cripts.core.cripts_mongoengine import CriptsDocumentFormatter
from cripts.core.cripts_mongoengine import CommonAccess
from cripts.core.cripts_mongoengine import CriptsActionsDocument
from cripts.hashes.migrate import migrate_hash


class Hash(CriptsBaseAttributes, CriptsSourceDocument, CriptsActionsDocument,
            Document):
    """
    Hash class.
    """

    meta = {
        "collection": settings.COL_HASHES,
        "cripts_type": 'Hash',
        "latest_schema_version": 1,
        "schema_doc": {
            'full_hash': 'Full hash, (including salt)',
            'source': ('List [] of sources who provided information about this'
                ' hash')
        },
        "jtable_opts": {
                         'details_url': 'cripts.hashes.views.view_dataset',
                         'details_url_key': 'id',
                         'default_sort': "created DESC",
                         'searchurl': 'cripts.hashes.views.hashes_listing',
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

    
class HashAccess(EmbeddedDocument, CriptsDocumentFormatter, CommonAccess):
    """
    ACL for Hashes
    """

    edit_details = BooleanField(default=False)    