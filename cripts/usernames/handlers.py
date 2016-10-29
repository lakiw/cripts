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
from cripts.core.cripts_mongoengine import create_embedded_source, json_handler
from cripts.services.handlers import run_triage, get_supported_services
from cripts.notifications.handlers import remove_user_from_notification

from cripts.usernames.username import UserName
from cripts.usernames.forms import UserNameForm


def generate_username_csv(request):
    """
    Generate a CSV file of the UserName information
    :param request: The request for this CSV.
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """

    response = csv_export(request,UserName)
    return response

def generate_username_jtable(request, option):
    """
    Generate the jtable data for rendering in the list template.
    :param request: The request for this jtable.
    :type request: :class:`django.http.HttpRequest`
    :param option: Action to take.
    :type option: str of either 'jtlist', 'jtdelete', or 'inline'.
    :returns: :class:`django.http.HttpResponse`
    """

    obj_type = UserName
    type_ = "username"
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
        'title': "UserNames",
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
            'tooltip': "'All UserNames'",
            'text': "'All'",
            'click': "function () {$('#eusername_listing').jtable('load', {'refresh': 'yes'});}",
            'cssClass': "'jtable-toolbar-center'",
        },
        {
            'tooltip': "'New UserNames'",
            'text': "'New'",
            'click': "function () {$('#username_listing').jtable('load', {'refresh': 'yes', 'status': 'New'});}",
            'cssClass': "'jtable-toolbar-center'",
        },
        {
            'tooltip': "'Add Username'",
            'text': "'Add Username'",
            'click': "function () {$('#new-username').click()}",
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
   
   
def parse_row_to_bound_username_form(request, rowData, cache):
    """
    Parse a row out of mass object username into the
    :class:`cripts.usernames.forms.UserNames`.
    :param request: The Django request.
    :type request: :class:`django.http.HttpRequest`
    :param rowData: The data for that row.
    :type rowData: dict
    :param cache: Cached data, typically for performance enhancements
                  during bulk operations.
    :type cache: dict
    :returns: :class:`cripts.usernames.forms.UserNameForm`.
    """
    name = rowData.get(form_consts.UserName.Name, "")
    description = rowData.get(form_consts.UserName.DESCRIPTION, "")
    analyst = request.user
    source = rowData.get(form_consts.UserName.SOURCE, "")
    source_method = rowData.get(form_consts.UserName.SOURCE_METHOD, "")
    source_reference = rowData.get(form_consts.UserName.SOURCE_REFERENCE, "")
    bucket_list = rowData.get(form_consts.Common.BUCKET_LIST, "")
    ticket = rowData.get(form_consts.Common.TICKET, "")
    data = {
        'name': name,
        'description': description,
        'analyst': analyst,
        'source': source,
        'source_method': source_method,
        'source_reference': source_reference,
        'bucket_list': bucket_list,
        'ticket': ticket}

    bound_form = cache.get('username_form')

    if bound_form == None:
        bound_form = UserNameForm(request.user, None, data)
        bound_form.data = data
        cache['username_form'] = bound_form
    else:
        bound_form.data = data

    bound_form.full_clean()
    return bound_form

   
def process_bulk_add_usernames(request, formdict):
    """
    Performs the bulk add of usernames by parsing the request data. Batches
    some data into a cache object for performance by reducing large
    amounts of single database queries.
    :param request: Django request.
    :type request: :class:`django.http.HttpRequest`
    :param formdict: The form representing the bulk uploaded data.
    :type formdict: dict
    :returns: :class:`django.http.HttpResponse`
    """
    username_names = []
    cached_results = {}

    cleanedRowsData = convert_handsontable_to_rows(request)
    for rowData in cleanedRowsData:
        if rowData != None and rowData.get(form_consts.UserName.NAME) != None:
            username_names.append(rowData.get(form_consts.UserName.NAME).lower())
            
    username_results = UserName.objects(username__in=username_names)

    for username_result in username_results:
        cached_results[username_result.username] = username_result

    cache = {form_consts.UserName.CACHED_RESULTS: cached_results, 'cleaned_rows_data': cleanedRowsData}

    response = parse_bulk_upload(request, parse_row_to_bound_username_form, add_new_username_via_bulk, formdict, cache)
    
    return response


def add_new_username_via_bulk(data, rowData, request, errors, is_validate_only=False, cache={}):
    """
    Bulk add wrapper for the username() function.
    """

    return add_new_username(data, rowData, request, errors, is_validate_only=is_validate_only, cache=cache)
    
   
def add_new_username(data, rowData, request, errors, is_validate_only=False, cache={}):
    """
    Add a new UserName to CRIPTs.
    :param data: Data for the username.
    :type data: dict
    :param rowData: Extra data from rows used by mass object uploader.
    :type rowData: dict
    :param request: The request for adding this UserName.
    :type request: :class:`django.http.HttpRequest`
    :param errors: A list of current errors prior to processing this UserName.
    :type errors: list
    :param is_validate_only: Whether or not we should validate or add.
    :type is_validate_only: bool
    :param cache: Cached data, typically for performance enhancements
                  during bulk operations.
    :type cache: dict
    :returns: tuple with (<result>, <errors>, <retval>)
    """
    
    result = False

    username = data.get('username')
    description = data.get('description')
    analyst = data.get('analyst')
    source = data.get('source')
    method = data.get('method')
    reference = data.get('reference')
    bucket_list = data.get(form_consts.Common.BUCKET_LIST_VARIABLE_NAME)
    ticket = data.get(form_consts.Common.TICKET_VARIABLE_NAME)

    retVal = username_add_update(username, description,
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
                new_username = retVal.get('object')

                if new_username != None and is_validate_only == False:
                    objectDict = object_array_to_dict(objectData,
                                                      "UserName", new_username.id)
                else:
                    if new_username != None:
                        if new_username.id:
                            objectDict = object_array_to_dict(objectData,
                                                              "UserName", new_username.id)
                        else:
                            objectDict = object_array_to_dict(objectData,
                                                              "UserName", "")
                    else:
                        objectDict = object_array_to_dict(objectData,
                                                          "UserName", "")

                (obj_result,
                 errors,
                 obj_retVal) = validate_and_add_new_handler_object(
                        None, objectDict, request, errors, object_row_counter,
                        is_validate_only=is_validate_only, cache=cache)

                if not obj_result:
                    retVal['success'] = False

    return result, errors, retVal

 
def username_add_update(name, description, source=None, method='', reference='',
                  analyst=None, datasets=None, bucket_list=None, ticket=None,
                  is_validate_only=False, cache={}, related_id=None,
                  related_type=None, relationship_type=None):

    retVal = {}
    
    if not source:
        return {"success" : False, "message" : "Missing source information."}              
        
    is_item_new = False

    username_object = None
    cached_results = cache.get(form_consts.UserName.CACHED_RESULTS)

    if cached_results != None:
        username_object = cached_results.get(username)
    else:
        username_object = UserName.objects(name=name).first()
    
    if not username_object:
        username_object = UserName()
        username_object.name = name
        username_object.description = description
        is_item_new = True

        if cached_results != None:
            cached_results[username] = username_object

    if not username_object.description:
        username_object.description = description or ''
    elif username_object.description != description:
        username_object.description += "\n" + (description or '')

    if isinstance(source, basestring):
        source = [create_embedded_source(source,
                                         reference=reference,
                                         method=method,
                                         analyst=analyst)]

    if source:
        for s in source:
            username_object.add_source(s)
    else:
        return {"success" : False, "message" : "Missing source information."}

    if bucket_list:
        username_object.add_bucket_list(bucket_list, analyst)

    if ticket:
        username_object.add_ticket(ticket, analyst)

    related_obj = None
    if related_id:
        related_obj = class_from_id(related_type, related_id)
        if not related_obj:
            retVal['success'] = False
            retVal['message'] = 'Related Object not found.'
            return retVal

    resp_url = reverse('cripts.usernames.views.username_detail', args=[username_object.username_id])

    if is_validate_only == False:
        username_object.save(username=analyst)

        #set the URL for viewing the new data
        if is_item_new == True:
            
            # Update the username stats
            counts = mongo_connector(settings.COL_COUNTS)
            count_stats = counts.find_one({'name': 'counts'})
            if not count_stats:
                count_stats = {}
            if 'UserNames' not in count_stats:
                count_stats['UserNames'] = 0
            else:
                count_stats['UserNames'] = count_stats['UserNames'] + 1
            
            counts.update({'name': "counts"}, {'$set': {'counts': count_stats}}, upsert=True)
            
            retVal['message'] = ('Success! Click here to view the new UserName: '
                                 '<a href="%s">%s</a>' % (resp_url, username_object.name))
        else:
            message = ('Updated existing UserName: '
                                 '<a href="%s">%s</a>' % (resp_url, username_object.name))
            retVal['message'] = message
            retVal['status'] = form_consts.Status.DUPLICATE
            retVal['warning'] = message

    elif is_validate_only == True:
        if username_object.id != None and is_item_new == False:
            message = ('Warning: UserName already exists: '
                                 '<a href="%s">%s</a>' % (resp_url, username_object.name))
            retVal['message'] = message
            retVal['status'] = form_consts.Status.DUPLICATE
            retVal['warning'] = message

    if related_obj and username_object and relationship_type:
        relationship_type=RelationshipTypes.inverse(relationship=relationship_type)
        username_object.add_relationship(related_obj,
                              relationship_type,
                              analyst=analyst,
                              get_rels=False)
        username_object.save(username=analyst)

    # run username triage
    if is_item_new and is_validate_only == False:
        username_object.reload()
        run_triage(username_object, analyst)

    retVal['success'] = True
    retVal['object'] = username_object

    return retVal
    
    
def get_username_details(username_id, analyst):
    """
    Generate the data to render the UserName details template.

    :param username_id: The id of the username to get details for.
    :type username_id: str
    :param analyst: The user requesting this information.
    :type analyst: str
    :returns: template (str), arguments (dict)
    """

    template = None
    allowed_sources = user_sources(analyst)
    username_object = UserName.objects(username_id=username_id,
                           source__name__in=allowed_sources).first()
    if not username_object:
        error = ("Either no data exists for this username"
                 " or you do not have permission to view it.")
        template = "error.html"
        args = {'error': error}
        return template, args

    username_object.sanitize_sources(username="%s" % analyst,
                           sources=allowed_sources)

    # remove pending notifications for user
    remove_user_from_notification("%s" % analyst, username_object.id, 'UserName')

    # subscription
    subscription = {
            'type': 'UserName',
            'id': username_object.id,
            'subscribed': is_user_subscribed("%s" % analyst,
                                             'UserName',
                                             username_object.id),
    }

    #objects
    objects = username_object.sort_objects()

    #relationships
    relationships = username_object.sort_relationships("%s" % analyst, meta=True)

    # relationship
    relationship = {
            'type': 'UserName',
            'value': username_object.id
    }

    #comments
    comments = {'comments':username_object.get_comments(),
                'url_key':username_object.username_id}

    # favorites
    favorite = is_user_favorite("%s" % analyst, 'UserName', username_object.id)

    # services
    service_list = get_supported_services('UserName')

    # analysis results
    service_results = username_object.get_analysis_results()

    args = {'username': username_object,
            'objects': objects,
            'relationships': relationships,
            'comments': comments,
            'favorite': favorite,
            'relationship': relationship,
            'subscription': subscription,
            'name': username_object.name,
            'service_list': service_list,
            'service_results': service_results}

    return template, args

    
def username_remove(username_id, username):
    """
    Remove an UserName from CRIPTs.
    :param username_id: The ObjectId of the UserName to remove.
    :type username_id: str
    :param username: The user removing this UserName.
    :type username: str
    :returns: dict with keys "success" (boolean) and "message" (str) if failed.
    """

    if is_admin(username):
        username = UserName.objects(id=username_id).first()
        if username:
            username.delete(username=username)
            return {'success': True}
        else:
            return {'success':False, 'message':'Could not find UserName.'}
    else:
        return {'success':False, 'message': 'Must be an admin to remove'}    
        
        
def generate_username_id(name):
    """
    Generate an Username ID.

    :param name: The name of the user.
    :type UserName: :class:`cripts.usernames.username.UserName`
    :returns: `uuid.uuid4()`
    """

    return uuid.uuid4()