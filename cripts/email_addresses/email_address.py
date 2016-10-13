import uuid

from mongoengine import Document, StringField, UUIDField
from django.conf import settings

from cripts.core.cripts_mongoengine import CriptsBaseAttributes, CriptsSourceDocument
from cripts.core.cripts_mongoengine import CriptsActionsDocument


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
            'email_address_id': 'Unique email_address ID',
            'datasets': ('List [] of datasets this email_address'
                ' appeared in'),
            'domain': 'Domain of the e-mail address, eg test.com',
            'source': ('List [] of sources who provided information about this'
                ' email address')
        },
        "jtable_opts": {
                         'details_url': 'cripts.email_addresses.views.view_email_address',
                         'details_url_key': 'id',
                         'default_sort': "created DESC",
                         'searchurl': 'cripts.email_addresses.views.email_addresses_listing',
                         'fields': [ "addresses", "created",
                                     "source", "id"],
                         'jtopts_fields': [ "address",
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

    
