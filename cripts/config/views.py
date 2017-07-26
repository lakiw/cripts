import json
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


from cripts.config.config import CRIPTsConfig
from cripts.config.forms import ConfigGeneralForm, ConfigLDAPForm, ConfigSecurityForm, ConfigCriptsForm
from cripts.config.forms import ConfigLoggingForm, ConfigServicesForm, ConfigDownloadForm
from cripts.config.handlers import modify_configuration
from cripts.core.user_tools import user_can_view_data
from cripts.vocabulary.acls import GeneralACL

@user_passes_test(user_can_view_data)
def cripts_config(request):

    """
    Generate the CRIPTs Configuration template.

    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """

    cripts_config = CRIPTsConfig.objects().first()
    user = request.user

    if user.has_access_to(GeneralACL.CONTROL_PANEL_READ):
        if cripts_config:
            cripts_config = cripts_config.to_dict()
            cripts_config['allowed_hosts'] = ", ".join(cripts_config['allowed_hosts'])
            cripts_config['service_dirs'] = ", ".join(cripts_config['service_dirs'])
            config_general_form = ConfigGeneralForm(initial=cripts_config)
            config_LDAP_form = ConfigLDAPForm(initial=cripts_config)
            config_security_form = ConfigSecurityForm(initial=cripts_config)
            config_logging_form = ConfigLoggingForm(initial=cripts_config)
            config_services_form = ConfigServicesForm(initial=cripts_config)
            config_download_form = ConfigDownloadForm(initial=cripts_config)
            config_CRIPTs_form = ConfigCriptsForm(initial=cripts_config)
        else:
            config_general_form = ConfigGeneralForm()
            config_LDAP_form = ConfigLDAPForm()
            config_security_form = ConfigSecurityForm()
            config_logging_form = ConfigLoggingForm()
            config_services_form = ConfigServicesForm()
            config_download_form = ConfigDownloadForm()
            config_CRIPTs_form = ConfigCriptsForm()
        return render_to_response('config.html',
                                  {'config_general_form': config_general_form,
                                   'config_LDAP_form': config_LDAP_form,
                                   'config_security_form': config_security_form,
                                   'config_logging_form': config_logging_form,
                                   'config_services_form': config_services_form,
                                   'config_download_form': config_download_form,
                                   'config_CRIPTs_form': config_CRIPTs_form,},
                                  RequestContext(request))
    else:
        return render_to_response('error.html',
                                  {'error': 'User does not have permission to view Control Panel.'},
                                  RequestContext(request))
                                  
@user_passes_test(user_can_view_data)
def modify_config(request):
    """
    Modify the CRIPTs Configuration. Should be an AJAX POST.

    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """
    from django.forms.util import ErrorList

    # Get the current configuration, set as default unless user has permission to edit.
    cripts_config = CRIPTsConfig.objects().first()
    config_data = cripts_config.__dict__.get('_data')
    analyst = request.user.username
    user = request.user
    errors = []
    permission_error = False

    if request.method == "POST" and request.is_ajax():

        if user.has_access_to(GeneralACL.CONTROL_PANEL_GENERAL_EDIT):
            config_general_form = ConfigGeneralForm(request.POST)
        else:
            config_general_form = ConfigGeneralForm(config_data)
            permission_error = True
        if user.has_access_to(GeneralACL.CONTROL_PANEL_LDAP_EDIT):
            config_LDAP_form = ConfigLDAPForm(request.POST)
        else:
            config_LDAP_form = ConfigLDAPForm(config_data)
            permission_error = True
        if user.has_access_to(GeneralACL.CONTROL_PANEL_SECURITY_EDIT):
            config_security_form = ConfigSecurityForm(request.POST)
        else:
            new_allowed_hosts = []
            for host in config_data['allowed_hosts']:
                new_allowed_hosts.append(str(host))

            config_data['allowed_hosts'] = ','.join(new_allowed_hosts)


            config_security_form = ConfigSecurityForm(config_data)
            permission_error = True
        if user.has_access_to(GeneralACL.CONTROL_PANEL_LOGGING_EDIT):
            config_logging_form = ConfigLoggingForm(request.POST)
        else:
            config_logging_form = ConfigLoggingForm(config_data)
            permission_error = True
        if user.has_access_to(GeneralACL.CONTROL_PANEL_SYSTEM_SERVICES_EDIT):
            config_services_form = ConfigServicesForm(request.POST)
        else:
            new_service_dirs = []
            for directory in config_data['service_dirs']:
                new_service_dirs.append(str(directory))
            config_data['service_dirs'] = ','.join(new_service_dirs)

            config_services_form = ConfigServicesForm(config_data)
            permission_error = True
        if user.has_access_to(GeneralACL.CONTROL_PANEL_DOWNLOADING_EDIT):
            config_download_form = ConfigDownloadForm(request.POST)
        else:
            config_download_form = ConfigDownloadForm(config_data)
            permission_error = True
        if user.has_access_to(GeneralACL.CONTROL_PANEL_CRIPTS_EDIT):
            config_CRIPTs_form = ConfigCriptsForm(request.POST)
        else:
            config_CRIPTs_form = ConfigCriptsForm(config_data)
            permission_error = True

        forms = [config_general_form,
                 config_LDAP_form,
                 config_security_form,
                 config_logging_form,
                 config_services_form,
                 config_download_form,
                 config_CRIPTs_form]
        #Used in defining the error message displayed to the user
        errorStringDict = {
            "ConfigGeneralForm": "General",
            "ConfigLDAPForm": "LDAP",
            "ConfigSecurityForm": "Security",
            "ConfigLoggingForm": "Logging",
            "ConfigServicesForm": "Services",
            "ConfigDownloadForm": "Downloading",
            "ConfigCriptsForm": "CRIPTs",
        }

        #iterate over all the forms, checking if they're valid
        #if the form is valid, remove it from the errorStringDict
        for form in forms:
            if form.is_valid():
                formName = type(form).__name__
                errorStringDict.pop(formName, None)
            else:
                errors.extend(form.errors)

        #submit if the errorStringDict is empty
        if not errorStringDict and not permission_error:
            result = modify_configuration(forms, analyst)
            message = result['message']
        elif permission_error:
            message = "User does not have permission to edit form."
        elif len(errorStringDict) == 2:
            formsWithErrors = " and ".join(errorStringDict.values())
            message = "Invalid Form: The " + formsWithErrors + " tabs have errors."
        elif len(errorStringDict) > 1:      #if there are multiple tabs with errors, pluralize the error message
            formsWithErrors = ", ".join(errorStringDict.values())
            lastWhiteSpace = formsWithErrors.rfind(" ")
            formsWithErrors = formsWithErrors[:lastWhiteSpace] + " and " + formsWithErrors[lastWhiteSpace:]
            message = "Invalid Form: The " + formsWithErrors + " tabs have errors."
        else:   #if there is only one tab with errors, make the error message singular
            formsWithErrors = errorStringDict.values()[0]
            message = "Invalid Form: The " + formsWithErrors + " tab has errors."

        message = {'message': message,
                   'errors': errors}
        return HttpResponse(json.dumps(message), content_type="application/json")
    else:
        return render_to_response('error.html',
                                  {'error': 'Expected AJAX POST'},
                                  RequestContext(request))
