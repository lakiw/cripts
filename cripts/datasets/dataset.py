from mongoengine import Document, StringField
from django.conf import settings

from cripts.core.cripts_mongoengine import CriptsBaseAttributes, CriptsSourceDocument
from cripts.core.cripts_mongoengine import CriptsActionsDocument


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
                         'details_url_key': 'id',
                         'default_sort': "modified DESC",
                         'searchurl': 'cripts.datasets.views.datasets_listing',
                         'fields': [ "created", "modified",
                                     "source", "id", "status"],
                         'jtopts_fields': [ "name",
                                            "created",
                                            "modified",
                                            "source",
                                            "favorite",
                                            "status",
                                            "id"],
                         'hidden_fields': [],
                         'linked_fields': ["source", ],
                         'details_link': 'details',
                         'no_sort': ['details']
                       }

    }
    
    id = StringField(required=True)
    

    
