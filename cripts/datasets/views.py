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

from cripts.datasets.handlers import generate_dataset_jtable, generate_dataset_csv, dataset_add_update
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
            status of the bulk uploaded Email Addresses. This may include information
            such as Dataset Name that failed or successfully added. This may
            also contain helpful status messages about each operation.
    """
    
    if request.method == 'POST':
        form = DatasetForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            filedata = request.FILES['filedata']
            filename = filedata.name
            data = filedata.read() # XXX: Should be using chunks here.
            source = cleaned_data.get('source')
            method = cleaned_data.get('method')
            user = request.user.username

            #status = handle_email_list_file(filename, data, source, user,
            #                         method=method)
            status = {'success':True, 'message':'placeholder'}
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