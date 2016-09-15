from cripts.services.analysis_result import AnalysisResult
from cripts.comments.comment import Comment
from cripts.events.event import Event


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
    return "None"
    
def get_obj_type_from_string(objType):
    """
    Returns the Object type from the string saved to the table. This 
    is used in order to build the query to be run.
    Called by generate_search_for_saved_table and get_table_data
    """
    if objType == "Comment":
        return Comment
    elif objType == "Event":
        return Event
        
    return None
