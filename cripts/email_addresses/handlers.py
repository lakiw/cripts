import datetime
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

try:
    from mongoengine.base import ValidationError
except ImportError:
    from mongoengine.errors import ValidationError

from cripts.core.mongo_tools import mongo_connector
from cripts.core import form_consts
from cripts.core.user_tools import is_admin, user_sources, is_user_favorite
from cripts.core.user_tools import is_user_subscribed
from cripts.core.handlers import csv_export
from cripts.core.handlers import build_jtable, jtable_ajax_list, jtable_ajax_delete
from cripts.core.handsontable_tools import convert_handsontable_to_rows, parse_bulk_upload
from cripts.email_addresses.email_address import EmailAddress
from cripts.email_addresses.forms import EmailAddressForm
from cripts.core.cripts_mongoengine import create_embedded_source, json_handler
from cripts.services.handlers import run_triage, get_supported_services
from cripts.notifications.handlers import remove_user_from_notification
from cripts.core.class_mapper import class_from_value
from cripts.vocabulary.relationships import RelationshipTypes

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
            
            # Update the email stats
            counts = mongo_connector(settings.COL_COUNTS)
            count_stats = counts.find_one({'name': 'counts'})
            if not count_stats or ('counts' not in count_stats):
                count_stats = {'counts':{}}
            if 'Email Addresses' not in count_stats['counts']:
                count_stats['counts']['Email Addresses'] = 0
            else:
                count_stats['counts']['Email Addresses'] = count_stats['counts']['Email Addresses'] - 1                                
            counts.update({'name': "counts"}, {'$set': {'counts': count_stats['counts']}}, upsert=True) 
            
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
   
   
def parse_row_to_bound_email_form(request, rowData, cache):
    """
    Parse a row out of mass object email adder into the
    :class:`cripts.email_addresses.forms.EmailForm`.
    :param request: The Django request.
    :type request: :class:`django.http.HttpRequest`
    :param rowData: The data for that row.
    :type rowData: dict
    :param cache: Cached data, typically for performance enhancements
                  during bulk operations.
    :type cache: dict
    :returns: :class:`cripts.email_addresses.forms.EmailForm`.
    """

    address = rowData.get(form_consts.EmailAddress.EMAIL_ADDRESS, "")
    description = rowData.get(form_consts.EmailAddress.DESCRIPTION, "")
    analyst = request.user
    source = rowData.get(form_consts.EmailAddress.SOURCE, "")
    source_method = rowData.get(form_consts.EmailAddress.SOURCE_METHOD, "")
    source_reference = rowData.get(form_consts.EmailAddress.SOURCE_REFERENCE, "")
    bucket_list = rowData.get(form_consts.Common.BUCKET_LIST, "")
    ticket = rowData.get(form_consts.Common.TICKET, "")
    data = {
        'address': address,
        'description': description,
        'analyst': analyst,
        'source': source,
        'source_method': source_method,
        'source_reference': source_reference,
        'bucket_list': bucket_list,
        'ticket': ticket}

    bound_form = cache.get('email_form')

    if bound_form == None:
        bound_form = EmailAddressForm(request.user, None, data)
        bound_form.data = data
        cache['email_form'] = bound_form
    else:
        bound_form.data = data

    bound_form.full_clean()
    return bound_form

   
def process_bulk_add_email_addresses(request, formdict):
    """
    Performs the bulk add of email addreesses by parsing the request data. Batches
    some data into a cache object for performance by reducing large
    amounts of single database queries.
    :param request: Django request.
    :type request: :class:`django.http.HttpRequest`
    :param formdict: The form representing the bulk uploaded data.
    :type formdict: dict
    :returns: :class:`django.http.HttpResponse`
    """
    email_names = []
    cached_results = {}

    cleanedRowsData = convert_handsontable_to_rows(request)
    for rowData in cleanedRowsData:
        if rowData != None and rowData.get(form_consts.EmailAddress.EMAIL_ADDRESS) != None:
            email_names.append(rowData.get(form_consts.EmailAddress.EMAIL_ADDRESS).lower())
            
    email_results = EmailAddress.objects(address__in=email_names)

    for email_result in email_results:
        cached_results[email_result.address] = email_result

    cache = {form_consts.EmailAddress.CACHED_RESULTS: cached_results, 'cleaned_rows_data': cleanedRowsData}

    response = parse_bulk_upload(request, parse_row_to_bound_email_form, add_new_email_via_bulk, formdict, cache)
    
    return response


def add_new_email_via_bulk(data, rowData, request, errors, is_validate_only=False, cache={}):
    """
    Bulk add wrapper for the add_new_email_address() function.
    """

    return add_new_email_address(data, rowData, request, errors, is_validate_only=is_validate_only, cache=cache)
    
   
def add_new_email_address(data, rowData, request, errors, is_validate_only=False, cache={}):
    """
    Add a new Email Address to CRIPTs.
    :param data: Data for the email address.
    :type data: dict
    :param rowData: Extra data from rows used by mass object uploader.
    :type rowData: dict
    :param request: The request for adding this Email Address.
    :type request: :class:`django.http.HttpRequest`
    :param errors: A list of current errors prior to processing this Email Address.
    :type errors: list
    :param is_validate_only: Whether or not we should validate or add.
    :type is_validate_only: bool
    :param cache: Cached data, typically for performance enhancements
                  during bulk operations.
    :type cache: dict
    :returns: tuple with (<result>, <errors>, <retval>)
    """
    
    result = False

    address = data.get('address')
    description = data.get('description')
    analyst = data.get('analyst')
    source = data.get('source')
    method = data.get('method')
    reference = data.get('reference')
    bucket_list = data.get(form_consts.Common.BUCKET_LIST_VARIABLE_NAME)
    ticket = data.get(form_consts.Common.TICKET_VARIABLE_NAME)

    retVal = email_address_add_update(address, description,
            source=source,
            method=method,
            reference=reference,
            analyst=analyst,
            bucket_list=bucket_list,
            ticket=ticket,
            is_validate_only=is_validate_only,
            cache=cache)

    if not retVal['success']:
        errors.append(retVal.get('message'))
        retVal['message'] = ""

    # This block tries to add objects to the item
    if retVal['success'] == True or is_validate_only == True:
        result = True
        objectsData = rowData.get(form_consts.Common.OBJECTS_DATA)

        # add new objects if they exist
        if objectsData:
            objectsData = json.loads(objectsData)

            for object_row_counter, objectData in enumerate(objectsData, 1):
                new_email = retVal.get('object')

                if new_email != None and is_validate_only == False:
                    objectDict = object_array_to_dict(objectData,
                                                      "EmailAddress", new_email.id)
                else:
                    if new_email != None:
                        if new_email.id:
                            objectDict = object_array_to_dict(objectData,
                                                              "EmailAddress", new_email.id)
                        else:
                            objectDict = object_array_to_dict(objectData,
                                                              "EmailAddress", "")
                    else:
                        objectDict = object_array_to_dict(objectData,
                                                          "EmailAddress", "")

                (obj_result,
                 errors,
                 obj_retVal) = validate_and_add_new_handler_object(
                        None, objectDict, request, errors, object_row_counter,
                        is_validate_only=is_validate_only, cache=cache)

                if not obj_result:
                    retVal['success'] = False

    return result, errors, retVal

 
def email_address_add_update(address, description=None, source=None, method='', reference='',
                  analyst=None, datasets=None, bucket_list=None, ticket=None,
                  is_validate_only=False, cache={}, related_id=None,
                  related_type=None, relationship_type=None):

    retVal = {}
    
    if not source:
        return {"success" : False, "message" : "Missing source information."}              
                  
    # Parse out the e-mail address. Return an error if it looks invalid, (aka missing the @, has whitespace, etc)
    try:
        if ' ' in address:
            raise ValueError
        local_name, domain_part = address.strip().split('@', 1)
        if len(local_name) == 0 or len(domain_part) == 0:
            raise ValueError
        # lowercase the domain name and recreate the e-mail address
        address = '@'.join([local_name, domain_part.lower()])
    except ValueError:
        return {'success': False, 'message': "Invalid Email Address Format"}
        
    is_item_new = False

    email_object = None
    cached_results = cache.get(form_consts.EmailAddress.CACHED_RESULTS)

    if cached_results != None:
        email_object = cached_results.get(address)
    else:
        email_object = EmailAddress.objects(address=address).first()
    
    if not email_object:
        email_object = EmailAddress()
        email_object.address = address
        email_object.description = description
        email_object.local_name = local_name
        email_object.domain = domain_part.lower()
        is_item_new = True

        if cached_results != None:
            cached_results[address] = email_object

    if not email_object.description:
        email_object.description = description or ''
    elif email_object.description != description:
        if description:
            email_object.description += "\n" + (description or '')        
            
    if isinstance(source, basestring):
        source = [create_embedded_source(source,
                                         reference=reference,
                                         method=method,
                                         analyst=analyst)]

    if source:
        for s in source:
            email_object.add_source(s)
    else:
        return {"success" : False, "message" : "Missing source information."}

    
    ##--Create reference to the parant datasets
    if datasets != None:
        email_object.datasets.append(datasets)
    
    print("Email datasets--------")
    print(email_object.datasets)
    
    if bucket_list:
        email_object.add_bucket_list(bucket_list, analyst)

    if ticket:
        email_object.add_ticket(ticket, analyst)

    related_obj = None
    if related_id:
        related_obj = class_from_value(related_type, related_id)
        if not related_obj:
            retVal['success'] = False
            retVal['message'] = 'Related Object not found.'
            return retVal

    resp_url = reverse('cripts.email_addresses.views.email_address_detail', args=[email_object.address])

    if is_validate_only == False:
        email_object.save(username=analyst)

        #set the URL for viewing the new data
        if is_item_new == True:
            
            # Update the email stats
            counts = mongo_connector(settings.COL_COUNTS)
            count_stats = counts.find_one({'name': 'counts'})
            if not count_stats or ('counts' not in count_stats):
                count_stats = {'counts':{}}
            if 'Email Addresses' not in count_stats['counts']:
                count_stats['counts']['Email Addresses'] = 1
            else:
                count_stats['counts']['Email Addresses'] = count_stats['counts']['Email Addresses'] + 1
            
            counts.update({'name': "counts"}, {'$set': {'counts': count_stats['counts']}}, upsert=True)
            
            retVal['message'] = ('Success! Click here to view the new Email: '
                                 '<a href="%s">%s</a>' % (resp_url, email_object.address))
        else:
            message = ('Updated existing Email: '
                                 '<a href="%s">%s</a>' % (resp_url, email_object.address))
            retVal['message'] = message
            retVal['status'] = form_consts.Status.DUPLICATE
            retVal['warning'] = message

    elif is_validate_only == True:
        if email_object.id != None and is_item_new == False:
            message = ('Warning: Email already exists: '
                                 '<a href="%s">%s</a>' % (resp_url, email_object.address))
            retVal['message'] = message
            retVal['status'] = form_consts.Status.DUPLICATE
            retVal['warning'] = message

    if related_obj and email_object and relationship_type:
        relationship_type=RelationshipTypes.inverse(relationship=relationship_type)
        email_object.add_relationship(related_obj,
                              relationship_type,
                              analyst=analyst,
                              get_rels=False)
        email_object.save(username=analyst)

    # run email triage
    if is_item_new and is_validate_only == False:
        email_object.reload()
        run_triage(email_object, analyst)

    retVal['success'] = True
    retVal['object'] = email_object

    return retVal
    
    
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

    args = {'email_address': address_object,
            'objects': objects,
            'relationships': relationships,
            'comments': comments,
            'favorite': favorite,
            'relationship': relationship,
            'subscription': subscription,
            'address': address_object.address,
            'service_list': service_list,
            'service_results': service_results,
            'id': address_object.id}

    return template, args

#################################################################################
# Processess a file upload of email addresses
# The email address file should be plain text and newline seperated
#################################################################################    
def handle_email_list_file(filename, data, source, user, method=None):
    retVal = {}
    retVal['success'] = False
    retVal['message'] = 'No email addresses found in file'
    results_count = {'Added':0, 'Modified':0, 'Invalid':0}
    
    for address in data.splitlines():
        result = email_address_add_update(address, description=None, source=source, method=method, reference='',
                  analyst=user, datasets=None, bucket_list=None, ticket=None,
                  is_validate_only=False, cache={}, related_id=None,
                  related_type=None, relationship_type=None)
        
        ##--Update the statistics of the success of adding emails to the database--##        
        try:
            ##--If it was an invalid e-mail address
            if result['success'] == False:
                results_count['Invalid'] = results_count['Invalid'] + 1
            ##--If it was a valid e-mail address
            else:
                ##--If it was a duplicate
                if 'status' in result and result['status'] == form_consts.Status.DUPLICATE:
                    results_count['Modified'] = results_count['Modified'] + 1
                else:
                    results_count['Added'] = results_count['Added'] + 1
        except Exception as e:
            results_count['Invalid'] = results_count['Invalid'] + 1
            
    retVal['success'] = True
    retVal['message'] = "New emails: " + str(results_count['Added']) + "<br>Modified emails: " + str(results_count['Modified']) + "<br>Invalid Entries: " + str(results_count['Invalid'])
    
    return retVal