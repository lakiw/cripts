from django.conf import settings
from django import forms

from cripts.core import form_consts
from cripts.core.forms import add_bucketlist_to_form, add_ticket_to_form, SourceInForm
from cripts.core.widgets import CalWidget
from cripts.core.handlers import get_source_names, get_item_names
from cripts.core.user_tools import get_user_organization

from cripts.vocabulary.events import EventTypes
from cripts.vocabulary.relationships import RelationshipTypes
from cripts.vocabulary.acls import Common, EventACL

relationship_choices = [(c, c) for c in RelationshipTypes.values(sort=True)]

class EventForm(SourceInForm):
    """
    Django form for creating a new Event.
    """

    error_css_class = 'error'
    required_css_class = 'required'
    title = forms.CharField(widget=forms.TextInput, required=True)
    event_type = forms.ChoiceField(required=True, widget=forms.Select)
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': '30',
                                                               'rows': '3'}),
                                  required=False)
    occurrence_date = forms.DateTimeField(
        widget=CalWidget(format=settings.PY_DATETIME_FORMAT,
                         attrs={'class':'datetimeclass',
                                'size':'25',
                                'id':'id_occurrence_date'}),
        input_formats=settings.PY_FORM_DATETIME_FORMATS)

    related_id = forms.CharField(widget=forms.HiddenInput(), required=False, label=form_consts.Common.RELATED_ID)
    related_type = forms.CharField(widget=forms.HiddenInput(), required=False, label=form_consts.Common.RELATED_TYPE)
    relationship_type = forms.ChoiceField(required=False,
                                          label=form_consts.Common.RELATIONSHIP_TYPE,
                                          widget=forms.Select(attrs={'id':'relationship_type'}))

    def __init__(self, username, *args, **kwargs):
        super(EventForm, self).__init__(username, *args, **kwargs)

        self.fields['event_type'].choices = [
            (c,c) for c in EventTypes.values(sort=True)
        ]
        self.fields['relationship_type'].choices = relationship_choices
        self.fields['relationship_type'].initial = RelationshipTypes.RELATED_TO

        add_bucketlist_to_form(self)
        add_ticket_to_form(self)
