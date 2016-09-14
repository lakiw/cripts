import json
import re
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from cripts.config.config import CRIPTsConfig
from cripts.config.forms import ConfigGeneralForm, ConfigLDAPForm, ConfigSecurityForm, ConfigCriptsForm
from cripts.config.forms import ConfigLoggingForm, ConfigServicesForm, ConfigDownloadForm
from cripts.config.handlers import modify_configuration
from cripts.core.user_tools import user_is_admin

@user_passes_test(user_is_admin)
def cripts_config(request):
    """
    Generate the CRIPTs Configuration template.

    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """

    cripts_config = CRIPTsConfig.objects().first()
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
                               'config_CRIPTs_form': config_CRIPTs_form},
                              RequestContext(request))

@user_passes_test(user_is_admin)
def modify_config(request):
    """
    Modify the CRIPTs Configuration. Should be an AJAX POST.

    :param request: Django request object (Required)
    :type request: :class:`django.http.HttpRequest`
    :returns: :class:`django.http.HttpResponse`
    """

    if request.method == "POST" and request.is_ajax():
        config_general_form = ConfigGeneralForm(request.POST)
        config_LDAP_form = ConfigLDAPForm(request.POST)
        config_security_form = ConfigSecurityForm(request.POST)
        config_logging_form = ConfigLoggingForm(request.POST)
        config_services_form = ConfigServicesForm(request.POST)
        config_download_form = ConfigDownloadForm(request.POST)
        config_CRIPTs_form = ConfigCriptsForm(request.POST)

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

        analyst = request.user.username
        errors = []
        #iterate over all the forms, checking if they're valid
        #if the form is valid, remove it from the errorStringDict
        for form in forms:
            if form.is_valid():
                formName = type(form).__name__
                errorStringDict.pop(formName, None)
            else:
                errors.extend(form.errors)

        #submit if the errorStringDict is empty
        if not errorStringDict:
            result = modify_configuration(forms, analyst)
            message = result['message']
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
