from mongoengine import Document, StringField, ListField
from mongoengine import BooleanField, EmbeddedDocumentField
from django.conf import settings

from cripts.core.cripts_mongoengine import CriptsDocument, CriptsSchemaDocument
from cripts.services.analysis_result import AnalysisConfig


class CRIPTsService(CriptsDocument, CriptsSchemaDocument, Document):
    """
    CRIPTs Service class.
    """

    meta = {
        "cripts_type": "Service",
        "collection": settings.COL_SERVICES,
        "latest_schema_version": 1,
        "schema_doc": {
            'name': 'Name of the service',
            'config': 'Dicionary of configuration items',
            'compatability_mode': 'If this service should run in compatability mode',
            'description': 'Description of the service',
            'enabled': 'If this service is enabled',
            'run_on_triage': 'If this service runs on upload',
            'status': 'The status of this service',
            'supported_types': 'CRIPTs types this service supports',
            'version': 'Version string of this service',
        }
    }

    name = StringField(required=True)
    config = EmbeddedDocumentField(AnalysisConfig)
    compatability_mode = BooleanField()
    description = StringField()
    enabled = BooleanField()
    run_on_triage = BooleanField()
    status = StringField()
    supported_types = ListField(StringField())
    version = StringField()
