from tastypie import authorization, fields, http
from tastypie.authentication import MultiAuthentication
from tastypie.exceptions import ImmediateHttpResponse

from cripts.core.api import CRIPTsApiKeyAuthentication, CRIPTsSessionAuthentication
from cripts.core.api import CRIPTsAPIResource, MongoObject
from cripts.vocabulary.actors import ThreatTypes, Motivations
from cripts.vocabulary.actors import Sophistications, IntendedEffects
from cripts.vocabulary.confidence import Confidence
from cripts.vocabulary.events import EventTypes
from cripts.vocabulary.indicators import IndicatorTypes, IndicatorThreatTypes
from cripts.vocabulary.indicators import IndicatorAttackTypes, IndicatorCI
from cripts.vocabulary.ips import IPTypes
from cripts.vocabulary.kill_chain import KillChain
from cripts.vocabulary.objects import ObjectTypes
from cripts.vocabulary.relationships import RelationshipTypes
from cripts.vocabulary.sectors import Sectors
from cripts.vocabulary.status import Status

class VocabResource(CRIPTsAPIResource):
    """
    Class to handle everything related to the Vocabulary API.

    Currently supports GET.
    """

    category = fields.CharField(attribute="category")
    values = fields.ListField(attribute="values")

    class Meta:
        allowed_methods = ('get')
        resource_name = "vocab"
        authentication = MultiAuthentication(CRIPTsApiKeyAuthentication(),
                                             CRIPTsSessionAuthentication())
        authorization = authorization.Authorization()

    def obj_get_list(self, bundle=None, **kwargs):
        output = []
        vocab_classes = (ThreatTypes, Motivations, Sophistications,
                         IntendedEffects, Confidence, EventTypes,
                         IndicatorTypes, IndicatorThreatTypes,
                         IndicatorAttackTypes, IndicatorCI, IPTypes, KillChain,
                         ObjectTypes, RelationshipTypes, Sectors, Status)
        for class_ in vocab_classes:
            values = class_.values(sort=True)
            output.append(MongoObject(initial={'category': class_.__name__,
                                               'values': values}))
        return output

    def obj_get(self, bundle=None, **kwargs):
        category = kwargs['pk']
        try:
            class_ = globals()[category]
        except:
            msg = 'Vocabulary category "%s" does not exist' % category
            raise ImmediateHttpResponse(response=http.HttpBadRequest(msg))

        values = class_.values(sort=True)
        return MongoObject(initial={'category': category, 'values': values})
