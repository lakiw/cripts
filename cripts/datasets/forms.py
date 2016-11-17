from django.conf import settings
from django import forms

from cripts.core import form_consts
from cripts.core.forms import add_bucketlist_to_form, add_ticket_to_form
from cripts.core.widgets import CalWidget
from cripts.core.handlers import get_source_names, get_item_names
from cripts.core.user_tools import get_user_organization

class DatasetForm(forms.Form):
    """
    Django form for creating a new Email Address.
    """
    error_css_class = 'error'
    required_css_class = 'required'
    name = forms.CharField(widget=forms.TextInput, required=True,
                               label=form_consts.Dataset.NAME)
    filedata = forms.FileField(label="Dataset")
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': '30',
                                                               'rows': '3'}),
                                  label=form_consts.Dataset.DESCRIPTION, required=False)
    source = forms.ChoiceField(required=True,
                               widget=forms.Select(attrs={'class': 'no_clear'}),
                               label=form_consts.Dataset.SOURCE)
    method = forms.CharField(required=False, widget=forms.TextInput,
                             label=form_consts.Dataset.SOURCE_METHOD)
    reference = forms.CharField(required=False, widget=forms.TextInput,
                                label=form_consts.Dataset.SOURCE_REFERENCE)
                                

    def __init__(self, username, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)
        self.fields['source'].choices = [(c.name,
                                          c.name) for c in get_source_names(True,
                                                                               True,
                                                                               username)]
        self.fields['source'].initial = get_user_organization(username)
        
        add_bucketlist_to_form(self)
        add_ticket_to_form(self)
        