import logging

from mongoengine import Document
from mongoengine import StringField, IntField

from django.conf import settings

from cripts.core.migrate import migrate_bucket
from cripts.core.crits_mongoengine import CriptsDocument, CriptsSchemaDocument

logger = logging.getLogger(__name__)

class Bucket(CriptsDocument, CriptsSchemaDocument, Document):
    """
    CRIPTs Bucket Class
    """

    meta = {
        "collection": settings.COL_BUCKET_LISTS,
        "cripts_type": 'Bucketlist',
        "latest_schema_version": 2,
        "schema_doc": {
            'name': 'Bucketlist name',
            'Event': 'Integer',
        },
    }

    name = StringField(required=True)
    Event = IntField(default=0)

    def migrate(self):
        """
        Migrate to the latest schema version.
        """

        migrate_bucket(self)
