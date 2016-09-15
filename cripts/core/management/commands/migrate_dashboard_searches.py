from django.core.management.base import BaseCommand
from optparse import make_option
from cripts.dashboards.dashboard import SavedSearch

class Command(BaseCommand):
    """
    Script Class.
    """
    help = 'Creates the default dashboard.'

    def handle(self, *args, **options):
        """
        Script Execution.
        """
        migrate_all_searches()
        
def migrate_all_searches():
    multiplier = 2
    for search in SavedSearch.objects():
        if "left" in search and search.left > 0:
            search.col = search.left/multiplier
        elif search.isDefaultOnDashboard:
             convert_default_searches(search, "left")
        if "width" in search:
            search.sizex = search.width/multiplier
        elif search.isDefaultOnDashboard:
             convert_default_searches(search, "width")
        if search.isDefaultOnDashboard:
            convert_default_searches(search, "top")
        search.save()
    SavedSearch.objects().update(unset__left=1, unset__top=1, unset__width=1)
def convert_default_searches(search, field):
    title = search.name
    if field == "width":
        if title == "Counts":
            search.sizex = 10
        else:
            search.sizex = 50
    elif field == "left":
        search.col = 1
    elif field == "top":
        search.row = 1
        if title == "Counts":
            search.sizey == 13
         
    
