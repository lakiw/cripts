import uuid

from mongoengine import Document, StringField, UUIDField, BooleanField
from mongoengine import EmbeddedDocument
from django.conf import settings

from cripts.core.cripts_mongoengine import CriptsBaseAttributes
from cripts.core.cripts_mongoengine import CriptsSourceDocument
from cripts.core.cripts_mongoengine import CommonAccess, CriptsDocumentFormatter
from cripts.core.cripts_mongoengine import CriptsActionsDocument
from cripts.events.migrate import migrate_event

from cripts.vocabulary.events import EventTypes


class UnreleasableEventError(Exception):
    """
    Exception for attempting to release an event relationship that is
    unreleasable.
    """

    def __init__(self, value, **kwargs):
        self.message = "Relationship %s cannot be released to the event's \
releasability list." % value
        super(UnreleasableEventError, self).__init__(**kwargs)

    def __str__(self):
        return repr(self.message)

class Event(CriptsBaseAttributes, CriptsSourceDocument, CriptsActionsDocument,
            Document):
    """
    Event class.
    """

    meta = {
        "collection": settings.COL_EVENTS,
        "cripts_type": 'Event',
        "latest_schema_version": 3,
        "schema_doc": {
            'title': 'Title of this event',
            'event_id': 'Unique event ID',
            'event_type': 'Type of event based on Event Type options',
            'description': 'Description of the event',
            'source': ('List [] of sources who provided information about this'
                ' event')
        },
        "jtable_opts": {
                         'details_url': 'cripts.events.views.view_event',
                         'details_url_key': 'id',
                         'default_sort': "created DESC",
                         'searchurl': 'cripts.events.views.events_listing',
                         'fields': [ "title", "event_type", "created",
                                     "source", "status", "id"],
                         'jtopts_fields': [ "details",
                                            "title",
                                            "event_type",
                                            "created",
                                            "source",
                                            "status",
                                            "favorite",
                                            "id"],
                         'hidden_fields': [],
                         'linked_fields': ["source", "event_type"],
                         'details_link': 'details',
                         'no_sort': ['details']
                       }

    }

    title = StringField(required=True)
    event_type = StringField(required=True)
    # description also exists in CriptsBaseAttributes, but this one is required.
    description = StringField(required=True)
    event_id = UUIDField(binary=True, required=True, default=uuid.uuid4)

    def set_event_type(self, event_type):
        """
        Set the Event Type.

        :param event_type: The event type to set (must exist in DB).
        :type event_type: str
        """

        if event_type in EventTypes.values():
            self.event_type = event_type

    def migrate(self):
        """
        Migrate to the latest schema version.
        """

        migrate_event(self)


class EventAccess(EmbeddedDocument, CriptsDocumentFormatter, CommonAccess):
    """
    ACL for Events.
    """

    add_sample = BooleanField(default=False)

    title_edit = BooleanField(default=False)
    type_edit = BooleanField(default=False)
