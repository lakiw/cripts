from django.test import SimpleTestCase

from cripts.relationships.handlers import forge_relationship, update_relationship_reasons, update_relationship_confidences
from cripts.core.user import CRIPTsUser
from cripts.vocabulary.relationships import RelationshipTypes

TUSER_NAME = "test_user"
TUSER_PASS = "!@#j54kfeimn?>S<D"
TUSER_EMAIL = "test_user@example.com"
TUSER2_NAME = "second_testUser"
TUSER2_PASS = "!@#saasdfasfwefwe?>S<Dd"
TUSER2_EMAIL = "asdfsaser@example.com"
TCAMPAIGN1 = "Test_Campain1"
TCAMPAIGN2 = "Test_Campain2"
TRELATIONSHIP_TYPE = RelationshipTypes.RELATED_TO
TRELATIONSHIP_CONFIDENCE = 'high'
TRELATIONSHIP_NEW_CONFIDENCE = 'medium'
TRELATIONSHIP_NEW_REASON = "Because I Said So"

def prep_db():
    """
    Prep database for test.
    """
    clean_db()
    # Add User
    user = CRIPTsUser.create_user(
                          username=TUSER_NAME,
                          password=TUSER_PASS,
                          email=TUSER_EMAIL,
                          )
    user.save()
    user2 = CRIPTsUser.create_user(
                          username=TUSER2_NAME,
                          password=TUSER2_PASS,
                          email=TUSER2_EMAIL,
                          )
    user2.save()

    
def clean_db():
    """
    Clean database for test.
    """
    user = CRIPTsUser.objects(username=TUSER_NAME).first()
    if user:
        user.delete()
    user2 = CRIPTsUser.objects(username=TUSER2_NAME).first()
    if user2:
        user2.delete()
    
    
class RelationshipConfidenceAndReasonTests(SimpleTestCase):
    """
    Test Domain Handlers
    """
    def setUp(self):
        prep_db()
        self.user = CRIPTsUser.objects(username=TUSER_NAME).first()
        self.user2 = CRIPTsUser.objects(username=TUSER2_NAME).first()
        
       
    def tearDown(self):
        clean_db()
        
    def testCreateRelationship(self):
        return
        
    def testChangingReason(self):
        return
        
    def testChangingConfidence(self):
        return
