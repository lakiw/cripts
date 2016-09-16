import sys
import traceback

from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option

from cripts.config.config import CRIPTsConfig
from cripts.core.mongo_tools import mongo_find_one
from cripts.events.event import Event


from prep import prep_database

class Command(BaseCommand):
    """
    Script Class.
    """

    option_list = BaseCommand.option_list + (
        make_option("-a", "--migrate_all", action="store_true", dest="mall",
                    default=False,
                    help="Migrate all collections."), 
        make_option("-E", "--migrate_events", action="store_true",
                    dest="events",
                    default=False,
                    help="Migrate events."),        
    )
    help = 'Upgrades MongoDB to latest version using mass-migration.'

    def handle(self, *args, **options):
        """
        Script Execution.
        """

        lv = settings.CRIPTS_VERSION
        mall = options.get('mall')
        events = options.get('events')  

        if (not mall and 
            not events and):
            print "You must select something to upgrade. See '-h' for options."
            sys.exit(1)
        else:
            upgrade(lv, options)

def migrate_collection(class_obj, sort_ids):
    """
    Migrate a collection by opening each document. This will, by nature of the
    core functionality in `cripts.core.cripts_mongoengine` check the
    schema_version and migrate it if it is not the latest version.

    :param class_obj: The class to migrate documents for.
    :type class_obj: class that inherits from
                     :class:`cripts.core.cripts_mongoengine.CriptsBaseAttributes`
    :param sort_ids: If we should sort by ids ascending.
    :type sort_ids: boolean
    """

    # find all documents that don't have the latest schema version
    # and migrate those.
    version = class_obj._meta['latest_schema_version']

    print "\nMigrating %ss" % class_obj._meta['cripts_type']
    if sort_ids:
        docs = (
            class_obj.objects(schema_version__lt=version)
            .order_by('+id')
            .timeout(False)
        )
    else:
        docs = class_obj.objects(schema_version__lt=version).timeout(False)
        total = docs.count()

    if not total:
        print "\tNo %ss to migrate!" % class_obj._meta['cripts_type']
        return

    print "\tMigrated 0 of %d" % total,
    count = 0
    doc = None
    try:
        for doc in docs:
            if 'migrated' in doc._meta and doc._meta['migrated']:
                count += 1
            print "\r\tMigrated %d of %d" % (count, total),
        print ""
    except Exception as e:
        # Provide some basic info so admin can query their db and figure out
        # what bad data is blowing up the migration.
        print "\n\n\tAn error occurred during migration!"
        print "\tMigrated: %d" % count
        formatted_lines = traceback.format_exc().splitlines()
        print "\tError: %s" % formatted_lines[-1]
        if hasattr(e, 'tlo'):
            print "\tDocument ID: %s" % e.tlo
        else:
            doc_id = mongo_find_one(class_obj._meta.get('collection'),
                                    {'schema_version': {'$lt': version}}, '_id')
            print "\tDocument ID: %s" % doc_id.get('_id')
        if doc:
            print "\tLast ID: %s" % doc.id
        sys.exit(1)

def upgrade(lv, options):
    """
    Perform the upgrade.

    :param lv: The CRIPTs version we are running.
    :type lv: str
    :param options: The options passed in for what to upgrade.
    :type options: dict
    """

    # eventually we will do something to check to see what the current version
    # of the CRIPTs DB is so we can upgrade through several versions at once.
    # this is important if prep scripts need to be run for certain upgrades
    # to work properly.
    mall = options.get('mall')
    events = options.get('events')
    skip = options.get('skip')

    # run prep migrations
    if not skip:
        prep_database()

    # run full migrations
    if mall or events:
        migrate_collection(Event, sort_ids)

    # Always bump the version to the latest in settings.py
    config = CRIPTsConfig.objects()
    if len(config) > 1:
        print "You have more than one config object. This is really bad."
    else:
        config = config[0]
        config.cripts_version = settings.CRIPTS_VERSION
        config.save()
