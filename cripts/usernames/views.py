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

from cripts.usernames.handlers import username_add_update, get_username_details
from cripts.usernames.handlers import generate_username_jtable, generate_username_csv
from cripts.usernames.handlers import username_remove, process_bulk_add_username
from cripts.usernames.forms import UserNameForm


@user_passes_test(user_can_view_data)
def usernames_listing(request,option=None):
    """
    Generate UserName Listing template.
    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :param option: Whether we should generate a CSV (yes if option is "csv")
    :type option: str
    :returns: :class:`django.http.HttpResponse`
    """
    if option == "csv":
        return generate_username_csv(request)
    return generate_username_jtable(request, option)


@user_passes_test(user_can_view_data)
def add_username(request):
    """
    Add an username to CRIPTs. Should be an AJAX POST.

    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """
    if request.method == "POST" and request.is_ajax():
        username_form = UserNameForm(request.user, request.POST)
        if username_form.is_valid():
            data = username_form.cleaned_data
            result = username_add_update(name=data['name'],
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
                message = ('<div>Success! Click here to view the new UserName: <a '
                           'href="%s">%s</a></div>'
                           % (reverse('crits.usernames.views.username_detail',
                                      args=[result['object'].username_id]),
                              result['object'].username_id))
                result['message'].insert(0, message)
            return HttpResponse(json.dumps(result,
                                           default=json_handler),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'form': username_form.as_table(),
                                            'success': False}),
                                content_type="application/json")
    else:
        return render_to_response("error.html",
                                  {"error": "Expected AJAX POST"},
                                  RequestContext(request))
                
                
@user_passes_test(user_can_view_data)
def bulk_add_usernames(request):
    """
    Bulk add UserNames via a bulk upload form.
    Args:
        request: The Django context which contains information about the
            session and key/value pairs for the bulk add UserName request
    Returns:
        If the request is not a POST and not a Ajax call then:
            Returns a rendered HTML form for a bulk add of IPs
        If the request is a POST and a Ajax call then:
            Returns a response that contains information about the
            status of the bulk uploaded UserName. This may include information
            such as UserName that failed or successfully added. This may
            also contain helpful status messages about each operation.
    """

    formdict = form_to_dict(UserNameForm(request.user, None))

    if request.method == "POST" and request.is_ajax():
        response = process_bulk_add_usernames(request, formdict)

        return HttpResponse(json.dumps(response,
                            default=json_handler),
                            content_type="application/json")
    else:
        return render_to_response('bulk_add_default.html', {'formdict': formdict,
                                                            'title': "Bulk Add UserNames",
                                                            'table_name': 'username',
                                                            'local_validate_columns': [form_consts.UserName.USERNAME],
                                                            'is_bulk_add_objects': True}, RequestContext(request))

                                                            
@user_passes_test(user_can_view_data)
def username_detail(request, username_id):
    """
    Generate the UserName details page.

    :param request: Django request.
    :type request: :class:`django.http.HttpRequest`
    :param username_id: The username id to get details for.
    :type username_id: str
    :returns: :class:`django.http.HttpResponse`
    """

    template = "username_detail.html"
    analyst = request.user.username
    (new_template, args) = get_username_details(username_id,
                                              analyst)
    if new_template:
        template = new_template
        
    return render_to_response(template,
                              args,
                              RequestContext(request))
                              
                              
@user_passes_test(user_can_view_data)
def remove_username(request):
    """
    Remove an UserName. Should be an AJAX POST.
    :param request: Django request.
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """

    if request.method == "POST" and request.is_ajax():
        if is_admin(request.user):
            result = username_remove(request.POST['key'],
                               request.user.username)
            return HttpResponse(json.dumps(result),
                                content_type="application/json")
        error = 'You do not have permission to remove this item.'
        return render_to_response("error.html",
                                  {'error': error},
                                  RequestContext(request))
    return render_to_response('error.html',
                              {'error':'Expected AJAX/POST'},
                              RequestContext(request))