from django.core.management.base import BaseCommand

from cripts.core.bucket import Bucket
from cripts.core.class_mapper import class_from_type

class Command(BaseCommand):
    """
    Script Class.
    """

    def handle(self, *args, **options):
        """
        Script Execution.
        """

        buckets = {}

        types = ['Dataset', 'EmailAddress', 'Event','Hash',
                 'Target', 'Username']

        for otype in types:
            klass = class_from_type(otype)
            if not klass:
                continue
            objs = klass.objects().only('bucket_list')
            for obj in objs:
                for bucket in obj.bucket_list:
                    if not bucket:
                        continue # Avoid empty strings
                    if bucket not in buckets:
                        buckets[bucket] = Bucket()
                        buckets[bucket].name = bucket
                        setattr(buckets[bucket], otype, 1)
                    else:
                        buckets[bucket][otype] += 1

        # Drop all existing buckets
        Bucket.objects().delete()

        for bucket in buckets.values():
            bucket.save()
