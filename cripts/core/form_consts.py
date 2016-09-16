class Action():
    ACTION_TYPE = "Action type"
    BEGIN_DATE = "Begin date"
    ANALYST = "Analyst"
    END_DATE = "End date"
    PERFORMED_DATE = "Performed date"
    ACTIVE = "Active"
    REASON = "Reason"
    DATE = "Date"
    OBJECT_TYPES = "TLOs"
    PREFERRED = "Preferred TLOs"

class Common():
    BUCKET_LIST = "Bucket List"
    CAMPAIGN = "Campaign"
    CAMPAIGN_CONFIDENCE = "Campaign Confidence"
    OBJECTS_DATA = "Objects Data"
    SOURCE = "Source"
    SOURCE_REFERENCE = "Source Reference"
    SOURCE_METHOD = "Source Method"
    TICKET = "Ticket"

    CLASS_ATTRIBUTE = "class"

    BULK_SKIP = "bulkskip"
    BULK_REQUIRED = "bulkrequired"

    # class names
    Event = "Event"
    Object = "Object"

    RELATED_ID = "Related ID"
    RELATED_TYPE = "Related Type"
    RELATIONSHIP_TYPE = "Relationship Type"

    BUCKET_LIST_VARIABLE_NAME = "bucket_list"
    TICKET_VARIABLE_NAME = "ticket"

class Status():
    """
    Status fields/enumerations used in bulk upload.
    """

    STATUS_FIELD = "status";
    FAILURE = 0;
    SUCCESS = 1;
    DUPLICATE = 2;


class Event():
    """
    Constants for Events.
    """

    TITLE = "Title"
    SOURCE = Common.SOURCE
    SOURCE_METHOD = Common.SOURCE_METHOD
    SOURCE_REFERENCE = Common.SOURCE_REFERENCE


class NotificationType():
    ALERT = 'alert'
    ERROR = 'error'
    INFORMATION = 'information'
    NOTIFICATION = 'notification'
    SUCCESS = 'success'
    WARNING = 'warning'

    ALL = [ALERT, ERROR, INFORMATION, NOTIFICATION, SUCCESS, WARNING]


class Object():
    """
    Constants for Objects.
    """

    OBJECT_TYPE_INDEX = 0
    VALUE_INDEX = 1
    SOURCE_INDEX = 2
    METHOD_INDEX = 3
    REFERENCE_INDEX = 4
    ADD_INDICATOR_INDEX = 5

    OBJECT_TYPE = "Object Type"
    VALUE = "Value"
    SOURCE = Common.SOURCE
    METHOD = "Method"
    REFERENCE = "Reference"
    PARENT_OBJECT_TYPE = "Otype"
    PARENT_OBJECT_ID = "Oid"



def get_source_field_for_class(otype):
    """
    Based on the CRIPTs type, get the source field constant.

    :param otype: The CRIPTs type.
    :type otype: str.
    :returns: str
    """

    class_to_source_field_map = {
        Common.Event: Event.SOURCE,
        Common.Object: Object.SOURCE,
    }
    return class_to_source_field_map.get(otype)
