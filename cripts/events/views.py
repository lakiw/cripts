import json
import urllib

from django import forms
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from cripts.core import form_consts
from cripts.core.user_tools import user_can_view_data
from cripts.events.forms import EventForm
from cripts.events.handlers import event_remove
from cripts.events.handlers import update_event_title, update_event_type
from cripts.events.handlers import get_event_details
from cripts.events.handlers import generate_event_jtable, add_sample_for_event
from cripts.events.handlers import generate_event_csv, add_new_event

from cripts.vocabulary.events import EventTypes
from cripts.vocabulary.acls import EventACL


@user_passes_test(user_can_view_data)
def events_listing(request, option=None):
    """
    Generate Event Listing template.

    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :param option: Whether or not we should generate a CSV (yes if option is "csv")
    :type option: str
    :returns: :class:`django.http.HttpResponse`
    """
    user = request.user

    if user.has_access_to(EventACL.READ):
        if option == "csv":
            return generate_event_csv(request)
        return generate_event_jtable(request, option)
    else:
        return render_to_response("error.html",
                                  {'error': 'User does not have permission to view Event listing.'},
                                  RequestContext(request))


@user_passes_test(user_can_view_data)
def add_event(request):
    """
    Add an event to CRIPTs. Should be an AJAX POST.

    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """

    user = request.user

    if request.method == "POST" and request.is_ajax():
        if user.has_access_to(EventACL.WRITE):
            event_form = EventForm(request.user, request.POST)
            if event_form.is_valid():
                data = event_form.cleaned_data
                result = add_new_event(title=data['title'],
                                       description=data['description'],
                                       event_type=data['event_type'],
                                       source_name=data['source_name'],
                                       source_method=data['source_method'],
                                       source_reference=data['source_reference'],
                                       source_tlp=data['source_tlp'],
                                       date=data['occurrence_date'],
                                       bucket_list=data[form_consts.Common.BUCKET_LIST_VARIABLE_NAME],
                                       ticket=data[form_consts.Common.TICKET_VARIABLE_NAME],
                                       user=request.user,
                                       related_id=data['related_id'],
                                       related_type=data['related_type'],
                                       relationship_type=data['relationship_type'])
                if 'object' in result:
                    del result['object']
                return HttpResponse(json.dumps(result), content_type="application/json")
            else:
                return HttpResponse(json.dumps({'form': event_form.as_table(),
                                                'success': False}),
                                    content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success':False,
                                            'message':'User does not have permission to add event.'}))
    else:
        return render_to_response("error.html",
                                  {"error": "Expected AJAX POST"},
                                  RequestContext(request))


@user_passes_test(user_can_view_data)
def event_search(request):
    """
    Search for events.

    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponseRedirect`
    """

    query = {}
    query[request.GET.get('search_type', '')] = request.GET.get('q', '').strip()
    return HttpResponseRedirect(reverse('cripts.events.views.events_listing') +
                                "?%s" % urllib.urlencode(query))


@user_passes_test(user_can_view_data)
def view_event(request, eventid):
    """
    View an Event.

    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :param eventid: The ObjectId of the event to get details for.
    :type eventid: str
    :returns: :class:`django.http.HttpResponse`
    """

    request.user._setup()
    user = request.user

    if user.has_access_to(EventACL.READ):
        template = 'event_detail.html'
        (new_template, args) = get_event_details(eventid, user)
        if new_template:
            template = new_template
        return render_to_response(template,
                                  args,
                                  RequestContext(request))
    else:
        return render_to_response("error.html",
                                  {'error': 'User does not have permission to view Event Details.'},
                                  RequestContext(request))


@user_passes_test(user_can_view_data)
def remove_event(request, _id):
    """
    Remove an Event.

    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :param _id: The ObjectId of the event to remove.
    :type _id: str
    :returns: :class:`django.http.HttpResponse`, :class:`django.http.HttpResponse`
    """

    user = request.user

    if user.has_access_to(EventACL.DELETE):
        result = event_remove(_id, '%s' % user.username)
    else:
        result['success'] = False
        result['message'] = "User does not have permission to remove Event."

    if result['success']:
        return HttpResponseRedirect(
            reverse('cripts.events.views.events_listing')
        )

    else:
        return render_to_response('error.html',
                                  {'error': result['message']},
                                  RequestContext(request))


@user_passes_test(user_can_view_data)
def set_event_title(request, event_id):
    """
    Set event title. Should be an AJAX POST.

    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :param event_id: The ObjectId of the event to update.
    :type event_id: str
    :returns: :class:`django.http.HttpResponse`
    """

    user = request.user

    if request.method == 'POST':
        if user.has_access_to(EventACL.TITLE_EDIT):
            title = request.POST.get('title', None)
            return HttpResponse(json.dumps(update_event_title(event_id,
                                                              title,
                                                              user.username)),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success':False,
                                            'message':'User does not have permission to edit event title.'}))
    else:
        error = "Expected POST"
        return render_to_response("error.html",
                                  {"error": error},
                                  RequestContext(request))


@user_passes_test(user_can_view_data)
def set_event_type(request, event_id):
    """
    Set event type. Should be an AJAX POST.

    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :param event_id: The ObjectId of the event to update.
    :type event_id: str
    :returns: :class:`django.http.HttpResponse`
    """

    if request.method == 'POST':
        user = request.user
        if user.has_access_to(EventACL.TYPE_EDIT):
            event_type = request.POST.get('type', None)
            return HttpResponse(json.dumps(update_event_type(event_id,
                                                             event_type,
                                                             user.username)),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success':False,
                                            'message':'User does not have permission to edit event type.'}))
    else:
        error = "Expected POST"
        return render_to_response("error.html",
                                  {"error": error},
                                  RequestContext(request))


@user_passes_test(user_can_view_data)
def get_event_type_dropdown(request):
    """
    Get a list of available event types.

    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """

    if request.is_ajax():
        e_types = EventTypes.values(sort=True)
        result = {'types': e_types}
        return HttpResponse(json.dumps(result),
                            content_type="application/json")
    else:
        error = "Expected AJAX"
        return render_to_response("error.html",
                                    {"error": error},
                                    RequestContext(request))
