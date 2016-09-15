from django.core.management.base import BaseCommand

from cripts.core.sector import Sector
from cripts.core.class_mapper import class_from_type

class Command(BaseCommand):
    """
    Script Class.
    """

    def handle(self, *args, **options):
        """
        Script Execution.
        """

        sectors = {}

        types = ['Event',
                 ]

        for otype in types:
            klass = class_from_type(otype)
            if not klass:
                continue
            objs = klass.objects().only('sectors')
            for obj in objs:
                for sector in obj.sectors:
                    if not sector:
                        continue # Avoid empty strings
                    if sector not in sectors:
                        sectors[sector] = Sector()
                        sectors[sector].name = sector
                        setattr(sectors[sector], otype, 1)
                    else:
                        sectors[sector][otype] += 1

        # Drop all existing sectors
        Sector.objects().delete()

        for sector in sectors.values():
            sector.save()
