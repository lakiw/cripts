import os

from django.conf import settings
from django.core.management.base import BaseCommand
from optparse import make_option

from create_indexes import create_indexes
from setconfig import create_config_if_not_exist
from create_default_dashboard import create_dashboard

from cripts.core.cripts_mongoengine import Action
from cripts.core.user_role import UserRole


class Command(BaseCommand):
    """
    Script Class.
    """

    option_list = BaseCommand.option_list + (
        make_option('--drop',
                    '-d',
                    dest='drop',
                    action="store_true",
                    default=False,
                    help='Drop existing content before adding.'),
    )
    help = 'Creates default CRIPTs collections in MongoDB.'

    def handle(self, *args, **options):
        """
        Script Execution.
        """

        drop = options.get('drop')
        if drop:
            print "Dropping enabled. Will drop content before adding!"
        else:
            print "Drop protection enabled. Will not drop existing content!"
        populate_user_roles(drop)
        populate_actions(drop)

        # The following will always occur with every run of this script:
        create_dashboard(drop)
        create_config_if_not_exist()
        create_indexes()


def populate_user_roles(drop):
    """
    Populate default set of user roles into the system.

    :param drop: Drop the existing collection before trying to populate.
    :type: boolean
    """

    # define your user roles here
    # note: you MUST have Administrator, Read Only, and a third option
    # available!
    user_roles = ['Administrator', 'Analyst', 'Read Only']
    if drop:
        UserRole.drop_collection()
    if len(UserRole.objects()) < 1:
        for role in user_roles:
            ur = UserRole()
            ur.name = role
            ur.save()
        print "User Roles: added %s roles!" % len(user_roles)
    else:
        print "User Roles: existing documents detected. skipping!"

def populate_actions(drop):
    """
    Populate default set of Actions into the system.

    :param drop: Drop the existing collection before trying to populate.
    :type: boolean
    """

    # define your Actions here
    actions = ['Blocked Outbound At Firewall', 'Blocked Outbound At Desktop Firewall']
    if drop:
        Action.drop_collection()
    if len(Action.objects()) < 1:
        for action in actions:
            ia = Action()
            ia.name = action
            ia.save()
        print "Actions: added %s actions!" % len(actions)
    else:
        print "Actions: existing documents detected. skipping!"



