from bson import Code
import datetime

from django.conf import settings
from cripts.core.mongo_tools import mongo_connector



def generate_filetypes():
    """
    Generate filetypes mapreduce.
    """

    samples = mongo_connector(settings.COL_SAMPLES)
    m = Code('function() emit({filetype: this.mimetype} ,{count: 1});}) }', {})
    r = Code('function(k,v) { var count = 0; v.forEach(function(v) { count += v["count"]; }); return {count: count}; }', {})
    try:
        samples.map_reduce(m,r, settings.COL_FILETYPES)
    except:
        return


def generate_counts():
    """
    Generate dashboard counts.
    """

    counts = mongo_connector(settings.COL_COUNTS)
    today = datetime.datetime.fromordinal(datetime.datetime.now().toordinal())
    start = datetime.datetime.now()
    last_seven = start - datetime.timedelta(7)
    last_thirty = start - datetime.timedelta(30)
    count = {}

    counts.update({'name': "counts"}, {'$set': {'counts': count}}, upsert=True)
