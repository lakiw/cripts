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
from cripts.datasets.dataset import Dataset
from cripts.core.cripts_mongoengine import create_embedded_source, json_handler
from cripts.notifications.handlers import remove_user_from_notification
from cripts.services.handlers import run_triage, get_supported_services
from cripts.datasets.forms import DatasetForm
from cripts.core.class_mapper import class_from_value
from cripts.vocabulary.relationships import RelationshipTypes

from cripts.usernames.handlers import username_add_update
from cripts.email_addresses.handlers import email_address_add_update

def generate_dataset_csv(request):
    """
    Generate a CSV file of the Dataset information
    :param request: The request for this CSV.
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """

    response = csv_export(request,Dataset)
    return response

def generate_dataset_jtable(request, option):
    """
    Generate the jtable data for rendering in the list template.
    :param request: The request for this jtable.
    :type request: :class:`django.http.HttpRequest`
    :param option: Action to take.
    :type option: str of either 'jtlist', 'jtdelete', or 'inline'.
    :returns: :class:`django.http.HttpResponse`
    """

    obj_type = Dataset
    type_ = "dataset"
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
            
            # Update the dataset stats
            counts = mongo_connector(settings.COL_COUNTS)
            count_stats = counts.find_one({'name': 'counts'})
            if not count_stats or ('counts' not in count_stats):
                count_stats = {'counts':{}}
            if 'Datasets' not in count_stats['counts']:
                count_stats['counts']['Datasets'] = 0
            else:
                count_stats['counts']['Datasets'] = count_stats['counts']['Datasets'] - 1                                
            counts.update({'name': "counts"}, {'$set': {'counts': count_stats['counts']}}, upsert=True) 
            
            response = {"Result": "OK"}
        return HttpResponse(json.dumps(response,
                                       default=json_handler),
                            content_type="application/json")
    jtopts = {
        'title': "Datasets",
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
            'tooltip': "'All Datasets'",
            'text': "'All'",
            'click': "function () {$('#dataset_listing').jtable('load', {'refresh': 'yes','status': 'All'});}",
            'cssClass': "'jtable-toolbar-center'",
        },
        {
            'tooltip': "'New Datasets'",
            'text': "'New'",
            'click': "function () {$('#dataset_listing').jtable('load', {'refresh': 'yes', 'status': 'New'});}",
            'cssClass': "'jtable-toolbar-center'",
        },
        {
            'tooltip': "'In Progress Datasets'",
            'text': "'In Progress'",
            'click': "function () {$('#dataset_listing').jtable('load', {'refresh': 'yes', 'status': 'In Progress'});}",
            'cssClass': "'jtable-toolbar-center'",
        },
        {
            'tooltip': "'Analyzed Datasets'",
            'text': "'Analyzed'",
            'click': "function () {$('#dataset_listing').jtable('load', {'refresh': 'yes', 'status': 'Analyzed'});}",
            'cssClass': "'jtable-toolbar-center'",
        },
        {
            'tooltip': "'Deprecated Datasets'",
            'text': "'Deprecated'",
            'click': "function () {$('#dataset_listing').jtable('load', {'refresh': 'yes', 'status': 'Deprecated'});}",
            'cssClass': "'jtable-toolbar-center'",
        },
        {
            'tooltip': "'Add Dataset'",
            'text': "'Add Dataset'",
            'click': "function () {$('#new-dataset').click()}",
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
       
       
def dataset_add_update(name, hash_type, dataset_format, hash_data, description=None, source=None, method='', reference='',
                  analyst=None, bucket_list=None, ticket=None,
                  is_validate_only=False, cache={}, related_id=None,
                  related_type=None, relationship_type=None):

    retVal = {}           

    dataset_object = Dataset.objects(name=name).first()
    
    if dataset_object:
        resp_url = reverse('cripts.datasets.views.dataset_detail', args=[dataset_object.name])
        message = ('Warning: Dataset already exists: '
                                 '<a href="%s">%s</a>. Cannot add new dataset with this name.' % (resp_url, dataset_object.name))
        retVal['message'] = message
        retVal['success'] = False
        retVal['object'] = dataset_object
        return retVal
               
    dataset_object = Dataset()
    dataset_object.name = name
    dataset_object.description = description
    resp_url = reverse('cripts.datasets.views.dataset_detail', args=[dataset_object.name])

    if isinstance(source, basestring):
        source = [create_embedded_source(source,
                                         reference=reference,
                                         method=method,
                                         analyst=analyst)]

    if source:
        for s in source:
            dataset_object.add_source(s)
    else:
        return {"success" : False, "message" : "Missing source information."}

    if bucket_list:
        dataset_object.add_bucket_list(bucket_list, analyst)

    if ticket:
        dataset_object.add_ticket(ticket, analyst)

    related_obj = None
    if related_id:
        related_obj = class_from_value(related_type, related_id)
        if not related_obj:
            retVal['success'] = False
            retVal['message'] = 'Related Object not found.'
            return retVal
            
    if is_validate_only == False:
        dataset_object.save(username=analyst)
            
        # Update the dataset stats
        counts = mongo_connector(settings.COL_COUNTS)
        count_stats = counts.find_one({'name': 'counts'})
        if not count_stats or ('counts' not in count_stats):
            count_stats = {'counts':{}}
        if 'Datasets' not in count_stats['counts']:
            count_stats['counts']['Datasets'] = 1
        else:
            count_stats['counts']['Datasets'] = count_stats['counts']['Datasets'] + 1
        
        counts.update({'name': "counts"}, {'$set': {'counts': count_stats['counts']}}, upsert=True)
        
        retVal['message'] = ('Success! Click here to view the new Dataset: '
                             '<a href="%s">%s</a>' % (resp_url, dataset_object.name))


    if related_obj and dataset_object and relationship_type:
        print("Adding relationship")
        relationship_type=RelationshipTypes.inverse(relationship=relationship_type)
        dataset_object.add_relationship(related_obj,
                              relationship_type,
                              analyst=analyst,
                              get_rels=False)
        dataset_object.save(username=analyst)
        
    ##--Now parse the hash list--##
    num_valid_records = 0
    num_invalid_records = 0
    
    for line in hash_data.splitlines():
        hash, username, email = parse_dataset_file(line, dataset_format)
        
        ##--No valid records were returned
        if not hash and not username and not email:
            num_invalid_records = num_invalid_records + 1
            continue
            
        ##--Todo: Look if adding validate only makes sense first before adding them--##
        ##----That way we can check if the whole line is valid before adding parts of it        
         
        ##--Add the email address if needed --## 
        if email:
            add_status = email_address_add_update(address=email,
                           description=None,
                           source=source,
                           method=method,
                           reference=reference,
                           datasets = dataset_object.name,
                           related_id=None,
                           related_type=None,
                           relationship_type=None,
                           bucket_list=None,
                           ticket=None,
                           analyst=analyst)
         
        ##--Add the username if needed --##
        if username:
            add_status = username_add_update(username, description=None, source=source, method=method, reference=reference,
                  analyst=analyst, datasets=dataset_object.name, bucket_list=None, ticket=None,
                  is_validate_only=False, cache={}, related_id=None,
                  related_type=None, relationship_type=None )
            if add_status['success'] != True:
                ##--If weirdness happens exit quickly vs trying to parse garbage for other fields
                num_invalid_records = num_invalid_records + 1
                continue

        ##--This line was parsed correctly
        num_valid_records = num_valid_records + 1
        
    print("Valid records = " + str(num_valid_records))
    print("Invalid records = " + str(num_invalid_records))    
    # run dataset triage
    if is_validate_only == False:
        dataset_object.reload()
        run_triage(dataset_object, analyst)

    retVal['success'] = True
    retVal['object'] = dataset_object

    return retVal
    
    
################################################################
# Parses a single line of the uploaded dataset file
# -Returns the follwing values (None if not read)
# (hash), (username), (email) 
##############################################################3#
def parse_dataset_file(line, format):
    hash = None
    username = None
    email = None
    
    values = line.split("\t")
    ##--if it is hash only
    if format == '1':
        if len(values) == 1:
            hash = values[0]
            
    ##--If it is hash, email address
    elif format == '2':
        if len(values) == 2:
            hash = values[0]
            email = values[1]
            
    ##---If it is hash, username
    elif format == '3':
        print(len(values))
        print(values)
        if len(values) == 2:
            hash = values[0]
            username = values[1]
            
    ##---If it is hash, username, email
    elif format == '4':
        if len(values) == 3:
            hash = values[0]
            username = values[1]
            email = values[2]
            
    else:
        print("Error parsing the line")
        
    return hash, username, email
    

def get_dataset_details(name, analyst):
    """
    Generate the data to render the Dataset details template.

    :param name: The name of the dataset to get details for.
    :type name: str
    :param analyst: The user requesting this information.
    :type analyst: str
    :returns: template (str), arguments (dict)
    """

    template = None
    allowed_sources = user_sources(analyst)
    dataset_object = Dataset.objects(name = name,
                           source__name__in=allowed_sources).first()
    if not dataset_object:
        error = ("Either no data exists for this dataset"
                 " or you do not have permission to view it.")
        template = "error.html"
        args = {'error': error}
        return template, args

    dataset_object.sanitize_sources(username="%s" % analyst,
                           sources=allowed_sources)

    # subscription
    subscription = {
            'type': 'Dataset',
            'id': dataset_object.id,
            'subscribed': is_user_subscribed("%s" % analyst,
                                             'Dataset',
                                             dataset_object.id),
    }                       
                           
    #objects
    objects = dataset_object.sort_objects()

    #relationships
    relationships = dataset_object.sort_relationships("%s" % analyst, meta=True)

    # relationship
    relationship = {
            'type': 'Dataset',
            'value': dataset_object.id
    }

    #comments
    comments = {'comments': dataset_object.get_comments(),
                'url_key':dataset_object.name}

    # favorites
    favorite = is_user_favorite("%s" % analyst, 'Dataset', dataset_object.name)

    # services
    service_list = get_supported_services('Dataset')

    # analysis results
    service_results = dataset_object.get_analysis_results()

    args = {'dataset': dataset_object,
            'objects': objects,
            'relationships': relationships,
            'comments': comments,
            'favorite': favorite,
            'relationship': relationship,
            'subscription': subscription,
            'name': dataset_object.name,
            'service_list': service_list,
            'service_results': service_results,
            'id': dataset_object.id}

    return template, args