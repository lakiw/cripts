from cripts.core.cripts_mongoengine import CriptsDocument, CriptsSchemaDocument
from mongoengine import DynamicDocument, ListField, ObjectIdField, StringField, DictField, IntField, BooleanField

class SavedSearch(CriptsDocument, CriptsSchemaDocument, DynamicDocument):
    """
    savedSearch class
    """
    meta = {
        "collection": "saved_search",
        "cripts_type": "saved_search",
        "latest_schema_version": 1,
        "schema_doc": {}
    }
    name = StringField(required=True)
    dashboard = ObjectIdField(required=True)
    tableColumns = ListField(required=True)
    sortBy = DictField(required=False)
    searchTerm = StringField(required=False)
    objType =  StringField(required=False)
    top = IntField(required=False, default=-1)
    left = IntField(required=False, default=-1)
    width = IntField(required=False)
    maxRows = IntField(required=False)
    isDefaultOnDashboard = BooleanField(required=True, default=False)
    isPinned = BooleanField(required=True, default=True)
    
    sizex = IntField(required=True, default=50)
    sizey = IntField(required=True, default=8)
    row = IntField(required=True, default=1)
    col = IntField(required=True, default=1)

    def getSortByText(self):
        textString = "None"
        if self.sortBy:
            for col in self.tableColumns:
                if col["field"] == self.sortBy["field"]:
                    textString = col["caption"] + " - " + self.sortBy['direction'].upper()
                    break;
        return textString
    
class Dashboard(CritpsDocument, CriptsSchemaDocument, DynamicDocument):
    """
    dashboard class
    """
    meta = {
        "collection": "dashboard",
        "cripts_type": "dashboard",
        "latest_schema_version": 1,
        "schema_doc": {}
    }
    name = StringField(required=True)
    analystId = ObjectIdField(required=False)
    theme = StringField(required=True,default="default")
    isPublic = BooleanField(required=True, default=False)
    parent = ObjectIdField(required=False)
    hasParentChanged = BooleanField(required=True, default=False)