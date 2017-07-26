from mongoengine import Document, StringField
from mongoengine import BooleanField, EmbeddedDocument
from django.conf import settings

from cripts.core.cripts_mongoengine import CriptsBaseAttributes, CriptsSourceDocument
from cripts.core.cripts_mongoengine import CriptsDocumentFormatter
from cripts.core.cripts_mongoengine import CommonAccess
from cripts.core.cripts_mongoengine import CriptsActionsDocument
from cripts.datasets.migrate import migrate_dataset



class Dataset(CriptsBaseAttributes, CriptsSourceDocument, CriptsActionsDocument,
            Document):
    """
    Dataset class.
    """

    meta = {
        "collection": settings.COL_DATASETS,
        "cripts_type": 'Dataset',
        "latest_schema_version": 1,
        "schema_doc": {
            'name': 'Name of the dataset',
        },
        "jtable_opts": {
                         'details_url': 'cripts.datasets.views.dataset_detail',
                         'details_url_key': 'name',
                         'default_sort': "modified DESC",
                         'searchurl': 'cripts.datasets.views.datasets_listing',
                         'fields': [ "name", "created", "modified",
                                     "source", "status","id"],
                         'jtopts_fields': [ "name",
                                            "created",
                                            "modified",
                                            "source",
                                            "favorite",
                                            "status",
                                            "id"
                                            ],
                         'hidden_fields': [],
                         'linked_fields': ["source", ],
                         'details_link': 'name',
                         'no_sort': []
                       }

    }
    
    name = StringField(required=True)
    

class DatasetAccess(EmbeddedDocument, CriptsDocumentFormatter, CommonAccess):
    """
    ACL for Datasets
    """

    edit_details = BooleanField(default=False)       
