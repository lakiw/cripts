import uuid

from mongoengine import Document, StringField, UUIDField, ListField
from mongoengine import BooleanField, EmbeddedDocument
from django.conf import settings

from cripts.core.cripts_mongoengine import CriptsBaseAttributes, CriptsSourceDocument
from cripts.core.cripts_mongoengine import CriptsDocumentFormatter
from cripts.core.cripts_mongoengine import CommonAccess
from cripts.core.cripts_mongoengine import CriptsActionsDocument
from cripts.email_addresses.migrate import migrate_email_address


class EmailAddress(CriptsBaseAttributes, CriptsSourceDocument, CriptsActionsDocument,
            Document):
    """
    EmailAddress class.
    """

    meta = {
        "collection": settings.COL_EMAIL_ADDRESSES,
        "cripts_type": 'EmailAddress',
        "latest_schema_version": 1,
        "schema_doc": {
            'address': 'Email address, eg: test@test.com',
            'datasets': ('List [] of datasets this email_address'
                ' appeared in'),
            'domain': 'Domain of the e-mail address, eg test.com',
            'local_name': 'The front part of the e-mail address. Eg. "user" of user@test.com',
            'description': 'Description of the e-mail address',
            'source': ('List [] of sources who provided information about this'
                ' email address')
        },
        "jtable_opts": {
                         'details_url': 'cripts.email_addresses.views.email_address_detail',
                         'details_url_key': "address",
                         'default_sort': "address",
                         'searchurl': 'cripts.email_addresses.views.email_addresses_listing',
                         'fields': [ "address", "local_name", "domain", "created",
                                     "source", "id"],
                         'jtopts_fields': [ "address",
                                            "local_name",
                                            "domain",
                                            "created",
                                            "source",
                                            "favorite",
                                            "id"],
                         'hidden_fields': [],
                         'linked_fields': ["source","local_name","domain" ],
                         'details_link': "address",
                         'no_sort': []
                       }

    }
    address = StringField(required=True)
    description = StringField(required=True)
    domain = StringField(required=True)
    local_name = StringField(required=True)
    datasets = ListField(required=False)
  

class EmailAddressAccess(EmbeddedDocument, CriptsDocumentFormatter, CommonAccess):
    """
    ACL for EmailAddresses
    """

    edit_details = BooleanField(default=False)    