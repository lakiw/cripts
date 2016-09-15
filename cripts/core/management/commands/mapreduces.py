from django.core.management.base import BaseCommand
import cripts.stats.handlers as stats

class Command(BaseCommand):
    """
    Script Class.
    """

    help = "Runs mapreduces for CRIPTs."

    def handle(self, *args, **options):
        """
        Script Execution.
        """

        stats.generate_sources()
        stats.generate_filetypes()
        stats.generate_counts()
        stats.target_user_stats()

