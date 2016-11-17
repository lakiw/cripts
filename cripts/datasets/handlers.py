import datetime
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from cripts.core.handlers import csv_export
from cripts.core.handlers import build_jtable, jtable_ajax_list
from cripts.datasets.dataset import Dataset
from cripts.core.cripts_mongoengine import create_embedded_source, json_handler

from cripts.datasets.forms import DatasetForm

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
                                  
def dataset_add_update(name, description=None, source=None, method='', reference='',
                  analyst=None, bucket_list=None, ticket=None,
                  is_validate_only=False, cache={}, related_id=None,
                  related_type=None, relationship_type=None):

    retVal = {}
    
    if not source:
        return {"success" : False, "message" : "Missing source information."}              
        
    is_item_new = False

    dataset_object = None
    cached_results = cache.get(form_consts.Dataset.CACHED_RESULTS)

    if cached_results != None:
        dataset_object = cached_results.get(name)
    else:
        dataset_object = Dataset.objects(name=name).first()
    
    if not dataset_object:
        dataset_object = Dataset()
        dataset_object.name = name
        dataset_object.description = description

        is_item_new = True

        if cached_results != None:
            cached_results[name] = dataset_object

    if not dataset_object.description:
        dataset_object.description = description or ''
    elif dataset_object.description != description:
        if description:
            dataset_object.description += "\n" + (description or '')

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
        related_obj = class_from_id(related_type, related_id)
        if not related_obj:
            retVal['success'] = False
            retVal['message'] = 'Related Object not found.'
            return retVal

    resp_url = reverse('cripts.datasets.views.email_address_detail', args=[dataset_object.name])

    if is_validate_only == False:
        dataset_object.save(username=analyst)

        #set the URL for viewing the new data
        if is_item_new == True:
            
            # Update the email stats
            counts = mongo_connector(settings.COL_COUNTS)
            count_stats = counts.find_one({'name': 'counts'})
            if not count_stats or ('counts' not in count_stats):
                count_stats = {'counts':{}}
            if 'Datasets' not in count_stats['counts']:
                count_stats['counts']['Datasets'] = 0
            else:
                count_stats['counts']['Datasets'] = count_stats['counts']['Datasets'] + 1
            
            counts.update({'name': "counts"}, {'$set': {'counts': count_stats['counts']}}, upsert=True)
            
            retVal['message'] = ('Success! Click here to view the new Dataset: '
                                 '<a href="%s">%s</a>' % (resp_url, dataset_object.name))
        else:
            message = ('Updated existing Dataset: '
                                 '<a href="%s">%s</a>' % (resp_url, dataset_object.name))
            retVal['message'] = message
            retVal['status'] = form_consts.Status.DUPLICATE
            retVal['warning'] = message

    elif is_validate_only == True:
        if dataset_object.id != None and is_item_new == False:
            message = ('Warning: Dataset already exists: '
                                 '<a href="%s">%s</a>' % (resp_url, dataset_object.name))
            retVal['message'] = message
            retVal['status'] = form_consts.Status.DUPLICATE
            retVal['warning'] = message

    if related_obj and email_object and relationship_type:
        relationship_type=RelationshipTypes.inverse(relationship=relationship_type)
        dataset_object.add_relationship(related_obj,
                              relationship_type,
                              analyst=analyst,
                              get_rels=False)
        dataset_object.save(username=analyst)

    # run dataset triage
    if is_item_new and is_validate_only == False:
        dataset_object.reload()
        run_triage(dataset_object, analyst)

    retVal['success'] = True
    retVal['object'] = dataset_object

    return retVal