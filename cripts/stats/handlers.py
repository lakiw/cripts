from bson import Code
import datetime

from django.conf import settings
from cripts.core.mongo_tools import mongo_connector
                        

def generate_counts():
    """
    Generate dashboard counts.
    """

    counts = mongo_connector(settings.COL_COUNTS)
    email_addresses = mongo_connector(settings.COL_EMAIL_ADDRESSES)
    
    today = datetime.datetime.fromordinal(datetime.datetime.now().toordinal())
    start = datetime.datetime.now()
    last_seven = start - datetime.timedelta(7)
    last_thirty = start - datetime.timedelta(30)
    
    count = {}
    count['Email Addresses'] = email_addresses.find().count()
    count['UserNames'] = email_address.find().count()

    counts.update({'name': "counts"}, {'$set': {'counts': count}}, upsert=True)
