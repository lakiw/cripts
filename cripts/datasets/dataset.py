import uuid

from mongoengine import Document, StringField, UUIDField
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
            'source': ('List [] of sources who provided information about this'
                ' dataset')
        },
        "jtable_opts": {
                         'details_url': 'cripts.datasets.views.view_dataset',
                         'details_url_key': 'id',
                         'default_sort': "created DESC",
                         'searchurl': 'cripts.datasets.views.datasets_listing',
                         'fields': [ "created",
                                     "source", "id"],
                         'jtopts_fields': [
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

    
