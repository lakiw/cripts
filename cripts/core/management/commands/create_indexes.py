import pymongo
from django.core.management.base import BaseCommand

from django.conf import settings
from optparse import make_option

from cripts.core.mongo_tools import mongo_connector

class Command(BaseCommand):
    """
    Script Class.
    """

    option_list = BaseCommand.option_list + (
        make_option('--remove-indexes',
                    '-r',
                    action='store_true',
                    dest='remove',
                    default=False,
                    help='Remove all indexes. Does NOT create.'),
    )
    help = 'Creates indexes for MongoDB.'

    def handle(self, *args, **options):
        """
        Script Execution.
        """

        remove = options.get('remove')
        if remove:
            remove_indexes()
        else:
            create_indexes()

def remove_indexes():
    """
    Removes all indexes from all collections.
    """

    coll_list = [
                 settings.COL_BUCKET_LISTS,
                 settings.COL_COMMENTS,
                 settings.COL_NOTIFICATIONS,
                 '%s.files' % settings.COL_OBJECTS,
                 '%s.chunks' % settings.COL_OBJECTS,
                 ]

    for coll in coll_list:
        print "Removing index for: %s" % coll
        c = mongo_connector(coll)
        c.drop_indexes()

def create_indexes():
    """
    Creates the default set of indexes for the system. Depending on your use
    cases, as well as quantity of data, admins may wish to tweak these indexes
    to best fit their requirements.
    """

    print "Creating indexes (duplicates will be ignored automatically)"

    analysis_results = mongo_connector(settings.COL_ANALYSIS_RESULTS)
    analysis_results.ensure_index("service_name", background=True)
    analysis_results.ensure_index("object_type", background=True)
    analysis_results.ensure_index("object_id", background=True)
    analysis_results.ensure_index("start_date", background=True)
    analysis_results.ensure_index("finish_date", background=True)
    analysis_results.ensure_index("version", background=True)
    analysis_results.ensure_index("analysis_id", background=True)

    bucket_lists = mongo_connector(settings.COL_BUCKET_LISTS)
    bucket_lists.ensure_index("name", background=True)

    events = mongo_connector(settings.COL_EVENTS)
    events.ensure_index("objects.value", background=True)
    events.ensure_index("title", background=True)
    events.ensure_index("relationships.value", background=True)
    events.ensure_index("campaign.name", background=True)
    events.ensure_index("source.name", background=True)
    events.ensure_index("created", background=True)
    events.ensure_index("status", background=True)
    events.ensure_index("favorite", background=True)
    events.ensure_index("event_type", background=True)
    events.ensure_index("bucket_list", background=True)
 

    if settings.FILE_DB == settings.GRIDFS:
        objects_files = mongo_connector('%s.files' % settings.COL_OBJECTS)
        objects_files.ensure_index("md5", background=True)

        objects_chunks = mongo_connector('%s.chunks' % settings.COL_OBJECTS)
        objects_chunks.ensure_index([("files_id",pymongo.ASCENDING),
                                ("n", pymongo.ASCENDING)],
                               unique=True)

    notifications = mongo_connector(settings.COL_NOTIFICATIONS)
    notifications.ensure_index("obj_id", background=True)
    # auto-expire notifications after 30 days
    notifications.ensure_index("date", background=True,
                               expireAfterSeconds=2592000)
    notifications.ensure_index("users", background=True)
