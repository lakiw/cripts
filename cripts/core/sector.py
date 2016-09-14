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
        },
    }

    name = StringField(required=True)
    Event = IntField(default=0)

    def migrate(self):
        """
        Migrate to the latest schema version.
        """

        pass
