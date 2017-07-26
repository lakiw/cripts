import uuid

from mongoengine import Document, StringField, ListField, UUIDField
from mongoengine import BooleanField, EmbeddedDocument
from django.conf import settings

from cripts.core.cripts_mongoengine import CriptsBaseAttributes, CriptsSourceDocument
from cripts.core.cripts_mongoengine import CriptsDocumentFormatter
from cripts.core.cripts_mongoengine import CommonAccess
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
            'name': 'The actual username',
            'username_id': 'An ID corresponding to the username since using the raw username as the key can run into little bobby tables issues',
            'description': 'Description of the e-mail address',
            'datasets': ('List [] of datasets this username'
                ' appeared in'),
            'source': ('List [] of sources who provided information about this'
                ' username'),
        },
        "jtable_opts": {
                         'details_url': 'cripts.usernames.views.username_detail',
                         'details_url_key': 'username_id',
                         'default_sort': "name",
                         'searchurl': 'cripts.usernames.views.usernames_listing',
                         'fields': [ "name", "created",
                                     "source", "id", "username_id"],
                         'jtopts_fields': [ "name",
                                            "created",
                                            "source",
                                            "favorite",
                                            "id", "username_id"],
                         'hidden_fields': ["username_id", "id"],
                         'linked_fields': ["source", ],
                         'details_link': 'name',
                         'no_sort': []
                       }

    }
    
    name = StringField(required=True)
    description = StringField(required=True)
    username_id = UUIDField(binary=True, required=True, default=uuid.uuid4)
    datasets = ListField(required=False)

    
class UserNameAccess(EmbeddedDocument, CriptsDocumentFormatter, CommonAccess):
    """
    ACL for UserNames
    """

    edit_details = BooleanField(default=False)    
