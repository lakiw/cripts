import datetime
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

try:
    from mongoengine.base import ValidationError
except ImportError:
    from mongoengine.errors import ValidationError
    
from cripts.core.user_tools import is_admin, user_sources, is_user_favorite
from cripts.core.user_tools import is_user_subscribed
from cripts.core.handlers import csv_export
from cripts.core.handlers import build_jtable, jtable_ajax_list
from cripts.email_addresses.email_address import EmailAddress
from cripts.core.cripts_mongoengine import create_embedded_source, json_handler
from cripts.services.handlers import run_triage, get_supported_services
from cripts.notifications.handlers import remove_user_from_notification

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
        'listurl': reverse('cripts.%ses.views.%ses_listing' %
                           (type_, type_), args=('jtlist',)),
        'deleteurl': reverse('cripts.%ses.views.%ses_listing' %
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
                                   'button' : '%ses_tab' % type_},
                                  RequestContext(request))
    else:
        return render_to_response("%s_listing.html" % type_,
                                  {'jtable': jtable,
                                   'jtid': '%s_listing' % type_},
                                  RequestContext(request))
   
   
def add_new_email_address(address, description, source, method, reference,
                  analyst, datasets=None, bucket_list=None, ticket=None,
                  related_id=None,
                  related_type=None, relationship_type=None):
    """
    Add a new Email Address to CRIPTs.

    :param address: The actual e-mail address
    :type address: str
    :param description: Email Address description.
    :type description: str
    :param source: The source which provided this information.
    :type source: str
    :param method: THe method of acquiring this information.
    :type method: str
    :param reference: Reference to this data.
    :type reference: str
    :param analyst: The user adding this Email Address.
    :type analyst: str
    :param datasets: The dataset(s) to associate with this Email Address.
    :type: list[str]
    :param bucket_list: The bucket(s) to associate with this Email Address.
    :type: str
    :param ticket: Ticket to associate with this Email Address.
    :type ticket: str
    :returns: dict with keys "success" (boolean) and "message" (str)
    """
    result = dict()
    if not source:
        return {'success': False, 'message': "Missing source information."}

    email_address = EmailAddress()
    email_address.address = address
    email_address.domain = 'gmail.com'
    email_address.description = description

    s = create_embedded_source(name=source,
                               reference=reference,
                               method=method,
                               analyst=analyst)
    email_address.add_source(s)

    if bucket_list:
        email_address.add_bucket_list(bucket_list, analyst)

    if ticket:
        email_address.add_ticket(ticket, analyst)

    related_obj = None
    if related_id:
        related_obj = class_from_id(related_type, related_id)
        if not related_obj:
            retVal['success'] = False
            retVal['message'] = 'Related Object not found.'
            return retVal

    try:
        email_address.save(username=analyst)

        if related_obj and email_address and relationship_type:
            relationship_type=RelationshipTypes.inverse(relationship=relationship_type)
            email_address.add_relationship(related_obj,
                                  relationship_type,
                                  analyst=analyst,
                                  get_rels=False)
            email_address.save(username=analyst)

        # run email_address triage
        email_address.reload()
        run_triage(email_address, analyst)

        message = ('<div>Success! Click here to view the new email address: <a href='
                   '"%s">%s</a></div>' % (reverse('cripts.email_addresses.views.email_address_detail',
                                                  args=[email_address.address]),
                                          address))
        result = {'success': True,
                  'message': message,
                  'object': list(email_address)}

    except ValidationError, e:
        result = {'success': False,
                  'message': e}
    return result
    
def get_email_address_details(address, analyst):
    """
    Generate the data to render the Email Address details template.

    :param address: The name of the Address to get details for.
    :type address: str
    :param analyst: The user requesting this information.
    :type analyst: str
    :returns: template (str), arguments (dict)
    """

    template = None
    allowed_sources = user_sources(analyst)
    address_object = EmailAddress.objects(address=address,
                           source__name__in=allowed_sources).first()
    if not address_object:
        error = ("Either no data exists for this email address"
                 " or you do not have permission to view it.")
        template = "error.html"
        args = {'error': error}
        return template, args

    address_object.sanitize_sources(username="%s" % analyst,
                           sources=allowed_sources)

    # remove pending notifications for user
    remove_user_from_notification("%s" % analyst, address_object.id, 'EmailAddress')

    # subscription
    subscription = {
            'type': 'EmailAddress',
            'id': address_object.id,
            'subscribed': is_user_subscribed("%s" % analyst,
                                             'EmailAddress',
                                             address_object.id),
    }

    #objects
    objects = address_object.sort_objects()

    #relationships
    relationships = address_object.sort_relationships("%s" % analyst, meta=True)

    # relationship
    relationship = {
            'type': 'EmailAddress',
            'value': address_object.id
    }

    #comments
    comments = {'comments': address_object.get_comments(),
                'url_key':address_object.address}

    # favorites
    favorite = is_user_favorite("%s" % analyst, 'EmailAddress', address_object.id)

    # services
    service_list = get_supported_services('EmailAddress')

    # analysis results
    service_results = address_object.get_analysis_results()

    args = {'objects': objects,
            'relationships': relationships,
            'comments': comments,
            'favorite': favorite,
            'relationship': relationship,
            'subscription': subscription,
            'address': address_object,
            'service_list': service_list,
            'service_results': service_results}

    return template, args
