import datetime
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from cripts.core.handlers import csv_export
from cripts.core.handlers import build_jtable, jtable_ajax_list
from cripts.email_addresses.email_address import EmailAddress
from cripts.core.cripts_mongoengine import create_embedded_source, json_handler

def generate_email_address_csv(request):
    """
    Generate a CSV file of the Email Address information
    :param request: The request for this CSV.
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """

    response = csv_export(request,EmailAddress)
    return response

def generate_email_address_jtable(request, option):
    """
    Generate the jtable data for rendering in the list template.
    :param request: The request for this jtable.
    :type request: :class:`django.http.HttpRequest`
    :param option: Action to take.
    :type option: str of either 'jtlist', 'jtdelete', or 'inline'.
    :returns: :class:`django.http.HttpResponse`
    """

    obj_type = EmailAddress
    type_ = "email_address"
    mapper = obj_type._meta['jtable_opts']
    if option == "jtlist":
        # Sets display url
        details_url = mapper['details_url']
        details_url_key = mapper['details_url_key']
        fields = mapper['fields']
        response = jtable_ajax_list(obj_type,
                                    details_url,
                                    details_url_key,
                                    request,
                                    includes=fields)
        return HttpResponse(json.dumps(response,
                                       default=json_handler),
                            content_type="application/json")
    if option == "jtdelete":
        response = {"Result": "ERROR"}
        if jtable_ajax_delete(obj_type,request):
            response = {"Result": "OK"}
        return HttpResponse(json.dumps(response,
                                       default=json_handler),
                            content_type="application/json")
    jtopts = {
        'title': "Email Addresses",
        'default_sort': mapper['default_sort'],
        'listurl': reverse('cripts.%ss.views.%ss_listing' %
                           (type_, type_), args=('jtlist',)),
        'deleteurl': reverse('cripts.%ss.views.%ss_listing' %
                             (type_, type_), args=('jtdelete',)),
        'searchurl': reverse(mapper['searchurl']),
        'fields': mapper['jtopts_fields'],
        'hidden_fields': mapper['hidden_fields'],
        'linked_fields': mapper['linked_fields'],
        'details_link': mapper['details_link'],
        'no_sort': mapper['no_sort']
    }
    jtable = build_jtable(jtopts,request)
    jtable['toolbar'] = [
        {
            'tooltip': "'All Email Addresses'",
            'text': "'All'",
            'click': "function () {$('#email_address_listing').jtable('load', {'refresh': 'yes'});}",
            'cssClass': "'jtable-toolbar-center'",
        },
        {
            'tooltip': "'New Email Addresses'",
            'text': "'New'",
            'click': "function () {$('#email_address_listing').jtable('load', {'refresh': 'yes', 'status': 'New'});}",
            'cssClass': "'jtable-toolbar-center'",
        },
        {
            'tooltip': "'In Progress Email Addresess'",
            'text': "'In Progress'",
            'click': "function () {$('#email_address_listing').jtable('load', {'refresh': 'yes', 'status': 'In Progress'});}",
            'cssClass': "'jtable-toolbar-center'",
        },
        {
            'tooltip': "'Analyzed Email Addresses'",
            'text': "'Analyzed'",
            'click': "function () {$('#email_address_listing').jtable('load', {'refresh': 'yes', 'status': 'Analyzed'});}",
            'cssClass': "'jtable-toolbar-center'",
        },
        {
            'tooltip': "'Deprecated Email Addresses'",
            'text': "'Deprecated'",
            'click': "function () {$('#email_address_listing').jtable('load', {'refresh': 'yes', 'status': 'Deprecated'});}",
            'cssClass': "'jtable-toolbar-center'",
        },
        {
            'tooltip': "'Add Email Address'",
            'text': "'Add Email Address'",
            'click': "function () {$('#new-email_address').click()}",
        },
    ]
    if option == "inline":
        return render_to_response("jtable.html",
                                  {'jtable': jtable,
                                   'jtid': '%s_listing' % type_,
                                   'button' : '%ss_tab' % type_},
                                  RequestContext(request))
    else:
        return render_to_response("%s_listing.html" % type_,
                                  {'jtable': jtable,
                                   'jtid': '%s_listing' % type_},
                                  RequestContext(request))