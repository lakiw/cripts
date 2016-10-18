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

from cripts.email_addresses.handlers import generate_email_address_jtable, generate_email_address_csv
from cripts.email_addresses.forms import EmailAddressForm

@user_passes_test(user_can_view_data)
def email_addresses_listing(request,option=None):
    """
    Generate Email Addresses Listing template.
    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :param option: Whether we should generate a CSV (yes if option is "csv")
    :type option: str
    :returns: :class:`django.http.HttpResponse`
    """
    if option == "csv":
        return generate_email_address_csv(request)
    return generate_email_address_jtable(request, option)

def add_email_address(request):
    """
    Add an email address to CRIPTs. Should be an AJAX POST.

    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """
    print("adding email address")
    if request.method == "POST" and request.is_ajax():
        email_address_form = EmailAddressForm(request.user, request.POST)
        if event_form.is_valid():
            data = email_address.cleaned_data
#            result = add_new_event(title=data['title'],
#                                   description=data['description'],
#                                   event_type=data['event_type'],
#                                   source=data['source'],
#                                   method=data['method'],
#                                   reference=data['reference'],
#                                   date=data['occurrence_date'],
#                                   bucket_list=data[form_consts.Common.BUCKET_LIST_VARIABLE_NAME],
#                                   ticket=data[form_consts.Common.TICKET_VARIABLE_NAME],
#                                   analyst=request.user.username,
#                                   related_id=data['related_id'],
#                                   related_type=data['related_type'],
#                                   relationship_type=data['relationship_type'])
#            if 'object' in result:
#                del result['object']
            result = None
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'form': event_form.as_table(),
                                            'success': False}),
                                content_type="application/json")
    else:
        return render_to_response("error.html",
                                  {"error": "Expected AJAX POST"},
                                  RequestContext(request))