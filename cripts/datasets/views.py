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

from cripts.datasets.handlers import generate_dataset_jtable, generate_dataset_csv, dataset_add_update
from cripts.datasets.handlers import get_dataset_details
from cripts.datasets.forms import DatasetForm

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
    if option == "csv":
        return generate_dataset_csv(request)
    return generate_dataset_jtable(request, option)

    
@user_passes_test(user_can_view_data)
def upload_dataset(request):
    """
    Add/Upload Dataset.
    Args:
        request: The Django context which contains information about the
            session and key/value pairs for the Dataset request
    Returns:
        If the request is not a POST and not a Ajax call then:
            Returns a rendered HTML form for a bulk add of IPs
        If the request is a POST and a Ajax call then:
            Returns a response that contains information about the
            status of the bulk uploaded Datasets. This may include information
            such as Dataset Name that failed or successfully added. This may
            also contain helpful status messages about each operation.
    """
    
    if request.method == 'POST':
        form = DatasetForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            name = cleaned_data.get('name')
            description = cleaned_data.get('description')
            hash_type = cleaned_data.get('hash_type')
            dataset_format = cleaned_data.get('dataset_format')
            filedata = request.FILES['filedata']
            filename = filedata.name
            hash_data = filedata.read() # XXX: Should be using chunks here.
            source = cleaned_data.get('source')
            method = cleaned_data.get('method')
            user = request.user.username
            related_id = cleaned_data['related_id']
            related_type = cleaned_data['related_type']
            relationship_type = cleaned_data['relationship_type']
            
            status = dataset_add_update(name, hash_type, dataset_format, hash_data, description, source, method, reference='',
                  analyst=request.user.username, bucket_list=cleaned_data[form_consts.Common.BUCKET_LIST_VARIABLE_NAME], 
                  ticket=cleaned_data[form_consts.Common.TICKET_VARIABLE_NAME],
                  related_id=related_id,
                  related_type=related_type,
                  relationship_type=relationship_type,
                  is_validate_only=False)
                  
            if status['success']:
                return render_to_response('file_upload_response.html',
                                          {'response': json.dumps({'message': 'Dataset uploaded successfully!<br>' + status['message']}), 'success': True},
                                          RequestContext(request))
            else:
                return render_to_response('file_upload_response.html',
                                          {'response': json.dumps({ 'success': False,'message': status['message']})}
                                          , RequestContext(request))
            
        else:
            return render_to_response('file_upload_response.html',
                                      {'response': json.dumps({'success': False,
                                                               'form': form.as_table()})},
                RequestContext(request))
    else:
        return render_to_response('error.html',
                                  {'error': "Expected POST." + str(request.method)},
                                  RequestContext(request))
              
              
@user_passes_test(user_can_view_data)
def dataset_detail(request, name):
    """
    Generate the Dataset details page.

    :param request: Django request.
    :type request: :class:`django.http.HttpRequest`
    :param name: The dataset to get details for.
    :returns: :class:`django.http.HttpResponse`
    """

    template = "dataset_detail.html"
    analyst = request.user.username
    (new_template, args) = get_dataset_details(name,
                                              analyst)
    if new_template:
        template = new_template
        
    return render_to_response(template,
                              args,
                              RequestContext(request))