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

from cripts.core import form_consts
from cripts.core.user_tools import user_can_view_data

from cripts.email_addresses.handlers import add_new_email_address, get_email_address_details
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

@user_passes_test(user_can_view_data)
def add_email_address(request):
    """
    Add an email address to CRIPTs. Should be an AJAX POST.

    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """
    if request.method == "POST" and request.is_ajax():
        email_address_form = EmailAddressForm(request.user, request.POST)
        if email_address_form.is_valid():
            data = email_address_form.cleaned_data
            result = add_new_email_address(address=data['address'],
                                   description=data['description'],
                                   source=data['source'],
                                   method=data['method'],
                                   reference=data['reference'],
                                   datasets = None,
                                   bucket_list=data[form_consts.Common.BUCKET_LIST_VARIABLE_NAME],
                                   ticket=data[form_consts.Common.TICKET_VARIABLE_NAME],
                                   analyst=request.user.username)
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'form': email_address_form.as_table(),
                                            'success': False}),
                                content_type="application/json")
    else:
        return render_to_response("error.html",
                                  {"error": "Expected AJAX POST"},
                                  RequestContext(request))
                
                
@user_passes_test(user_can_view_data)
def email_address_detail(request, address):
    """
    Generate the Email Address details page.

    :param request: Django request.
    :type request: :class:`django.http.HttpRequest`
    :param address: The email address to get details for.
    :type address: str
    :returns: :class:`django.http.HttpResponse`
    """

    template = "email_address_detail.html"
    (new_template, args) = get_email_address_details(address,
                                              request.user.username)
    if new_template:
        template = new_template
    return render_to_response(template,
                              args,
                              RequestContext(request))
