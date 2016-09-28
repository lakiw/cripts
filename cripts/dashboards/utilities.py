from cripts.services.analysis_result import AnalysisResult
from cripts.comments.comment import Comment
from cripts.events.event import Event
from cripts.usernames.username import UserName
from cripts.targets.target import Target
from cripts.hashes.hash import Hash
from cripts.datasets.dataset import Dataset
from cripts.email_addresses.email_address import EmailAddress



def getHREFLink(object, object_type):
    """
    Creates the URL for the details button used by all object types
    """
    #comment is a special case since the link takes you to the object the comment is on 
    if object_type == "Comment":
        object_type = object["obj_type"]
    #setting the first part of the url, rawdata is the only object type thats 
    #difference from its type
    href = "/"
    
    if object_type == "AnalysisResult":
        href += "services/analysis_results/"
	elif object_type == "EmailAddress":
		href += "email_address/"
    else:
        href += object_type.lower()+"s/"
        
    #settings the second part of the url
    href += "details/"
    
    #setting the key for the last section of the url since its different for 
    #every object type
    if "url_key" in object:
        key = "url_key"
    else:
        key = "id"
        
    #adding the last part of the url 
    if key in object:
        href += unicode(object[key]) + "/"
    return href

def get_obj_name_from_title(tableTitle):
    """
    Returns the String pertaining to the type of the table. Used only 
    when editing a default dashboard table since they do not have types saved,
    it gets it from the hard-coded title.
    """
	if tableTitle == "Counts":
		return "Count"
    return "None"
    
def get_obj_type_from_string(objType):
    """
    Returns the Object type from the string saved to the table. This 
    is used in order to build the query to be run.
    Called by generate_search_for_saved_table and get_table_data
    """
	from cripts.usernames.username import UserName
from cripts.targets.target import Target
from cripts.hashes.hash import Hash
from cripts.datasets.dataset import Dataset
from cripts.email_addresses.email_address import EmailAddress

    if objType == "Comment":
        return Comment
    elif objType == "Event":
        return Event
	elif objType == "AnalysisResult":
		return AnalysisResult
	elif objType == "UserName":
		return UserName
	elif objType == "Target":
		return Target
	elif objType == "Hash":
		return Hash
	elif objType == "Dataset":
		return Dataset
	elif objType == "EmailAddress":
		return EmailAddress
        
    return None
