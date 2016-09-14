import datetime

from mongoengine import Document, StringField, ObjectIdField
from django.conf import settings

from cripts.core.cripts_mongoengine import CriptsDocument, CriptsSchemaDocument
from cripts.core.fields import CriptsDateTimeField


class AuditLog(CriptsDocument, CriptsSchemaDocument, Document):
    """
    Audit Log Class
    """
    meta = {
        "allow_inheritance": False,
        "cripts_type": "AuditLog",
        "collection": settings.COL_AUDIT_LOG,
        "latest_schema_version": 1,
        "schema_doc": {
            'value': 'Value of the audit log entry',
            'user': 'User the entry is about.',
            'date': 'Date of the entry',
            'type': 'Type of the audit entry',
            'method': 'Method of the audit entry'
        }
    }

    value = StringField()
    user = StringField()
    date = CriptsDateTimeField(default=datetime.datetime.now)
    target_type = StringField(db_field='type')
    target_id = ObjectIdField()
    method = StringField()
