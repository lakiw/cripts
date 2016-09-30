import logging

from mongoengine import Document
from mongoengine import StringField, IntField

from django.conf import settings

from cripts.core.cripts_mongoengine import CriptsDocument, CriptsSchemaDocument

logger = logging.getLogger(__name__)

class Sector(CriptsDocument, CriptsSchemaDocument, Document):
    """
    CRIPTs Sector Class
    """

    meta = {
        "collection": settings.COL_SECTOR_LISTS,
        "cripts_type": 'Sectorlist',
        "latest_schema_version": 1,
        "schema_doc": {
            'name': 'Sectorlist name',
            'Event': 'Integer',
            'UserName': 'Integer',
            'Target': 'Integer',
            'Hash': 'Integer',
            'Dataset': 'Integer',
            'EmailAddress': 'Integer',
        },
    }

    name = StringField(required=True)
    Event = IntField(default=0)
    UserName = IntField(default=0)
    Target = IntField(default=0)
    Hash = IntField(default=0)
    Dataset = IntField(default=0)
    EmailAddress = IntField(default=0)

    def migrate(self):
        """
        Migrate to the latest schema version.
        """

        pass
