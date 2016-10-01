import datetime
import json
import urllib

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

from cripts.core.user_tools import user_can_view_data

@user_passes_test(user_can_view_data)
def datasets_listing(request,option=None):
    """
    Generate Dataset Listing template.
    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :param option: Whether we should generate a CSV (yes if option is "csv")
    :type option: str
    :returns: :class:`django.http.HttpResponse`
    """
    return None
    #if option == "csv":
    #   return generate_email_csv(request)
    #return generate_email_jtable(request, option)

