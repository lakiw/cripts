import uuid

from mongoengine import Document, StringField, UUIDField, ListField
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
            'datasets': ('List [] of datasets this email_address'
                ' appeared in'),
            'domain': 'Domain of the e-mail address, eg test.com',
            'description': 'Description of the e-mail address',
            'source': ('List [] of sources who provided information about this'
                ' email address')
        },
        "jtable_opts": {
                         'details_url': 'cripts.email_addresses.views.email_address_detail',
                         'details_url_key': "address",
                         'default_sort': "address",
                         'searchurl': 'cripts.email_addresses.views.email_addresses_listing',
                         'fields': [ "address", "created",
                                     "source"],
                         'jtopts_fields': [ "address",
                                            "domain",
                                            "created",
                                            "source",
                                            "favorite"],
                         'hidden_fields': [],
                         'linked_fields': ["source","address" ],
                         'details_link': "address",
                         'no_sort': []
                       }

    }
    address = StringField(required=True)
    description = StringField(required=True)
    domain = StringField(required=True)
    datasets = ListField(required=False)
  
