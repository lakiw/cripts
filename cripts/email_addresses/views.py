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
from cripts.core.handsontable_tools import form_to_dict
from cripts.core.data_tools import json_handler

from cripts.email_addresses.handlers import email_address_add_update, get_email_address_details
from cripts.email_addresses.handlers import generate_email_address_jtable, generate_email_address_csv
from cripts.email_addresses.handlers import process_bulk_add_email_addresses, handle_email_list_file
from cripts.email_addresses.forms import EmailAddressForm, UploadEmailAddressForm

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
            result = email_address_add_update(address=data['address'],
                                   description=data['description'],
                                   source=data['source'],
                                   method=data['method'],
                                   reference=data['reference'],
                                   datasets = None,
                                   bucket_list=data[form_consts.Common.BUCKET_LIST_VARIABLE_NAME],
                                   ticket=data[form_consts.Common.TICKET_VARIABLE_NAME],
                                   analyst=request.user.username)
                                   
            if 'message' in result:
                if not isinstance(result['message'], list):
                    result['message'] = [result['message']]
            else:
                result['message'] = []
                message = ('<div>Success! Click here to view the new Email: <a '
                           'href="%s">%s</a></div>'
                           % (reverse('crits.email_addresses.views.email_address_detail',
                                      args=[result['object'].address]),
                              result['object'].address))
                result['message'].insert(0, message)
            return HttpResponse(json.dumps(result,
                                           default=json_handler),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'form': email_address_form.as_table(),
                                            'success': False}),
                                content_type="application/json")
    else:
        return render_to_response("error.html",
                                  {"error": "Expected AJAX POST"},
                                  RequestContext(request))
                
                
@user_passes_test(user_can_view_data)
def bulk_add_email_addresses(request):
    """
    Bulk add Email Addresses via a bulk upload form.
    Args:
        request: The Django context which contains information about the
            session and key/value pairs for the bulk add Email Addresses request
    Returns:
        If the request is not a POST and not a Ajax call then:
            Returns a rendered HTML form for a bulk add of IPs
        If the request is a POST and a Ajax call then:
            Returns a response that contains information about the
            status of the bulk uploaded Email Addresses. This may include information
            such as Email Address that failed or successfully added. This may
            also contain helpful status messages about each operation.
    """

    formdict = form_to_dict(EmailAddressForm(request.user, None))

    if request.method == "POST" and request.is_ajax():
        response = process_bulk_add_email_addresses(request, formdict)

        return HttpResponse(json.dumps(response,
                            default=json_handler),
                            content_type="application/json")
    else:
        return render_to_response('bulk_add_default.html', {'formdict': formdict,
                                                            'title': "Bulk Add Email Addressess",
                                                            'table_name': 'email_address',
                                                            'local_validate_columns': [form_consts.EmailAddress.EMAIL_ADDRESS],
                                                            'is_bulk_add_objects': True}, RequestContext(request))

                                                            
@user_passes_test(user_can_view_data)
def bulk_file_upload_email_addresses(request):
    """
    Bulk upload of Email Addresses via a file upload to CRIPTs.
    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """
    
    if request.method == 'POST':
        form = UploadEmailAddressForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            filedata = request.FILES['filedata']
            filename = filedata.name
            data = filedata.read() # XXX: Should be using chunks here.
            source = cleaned_data.get('source')
            method = cleaned_data.get('method')
            user = request.user.username

            status = handle_email_list_file(filename, data, source, user,
                                     method=method)
            if status['success']:
                return render_to_response('file_upload_response.html',
                                          {'response': json.dumps({'message': 'Email list uploaded successfully!<br>' + status['message']}), 'success': True},
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
    analyst = request.user.username
    (new_template, args) = get_email_address_details(address,
                                              analyst)
    if new_template:
        template = new_template
        
    return render_to_response(template,
                              args,
                              RequestContext(request))
                     