from cripts.vocabulary.vocab import vocab

class Common(vocab):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    DOWNLOAD = "download"

    ALIASES_READ = "aliases_read"
    ALIASES_EDIT = "aliases_edit"

    DESCRIPTION_READ = "description_read"
    DESCRIPTION_EDIT = "description_edit"

    ACTIONS_READ = "actions_read"
    ACTIONS_ADD = "actions_add"
    ACTIONS_EDIT = "actions_edit"
    ACTIONS_DELETE = "actions_delete"

    BUCKETLIST_READ = "bucketlist_read"
    BUCKETLIST_EDIT = "bucketlist_edit"

    COMMENTS_READ = "comments_read"
    COMMENTS_ADD = "comments_add"
    COMMENTS_EDIT = "comments_edit"
    COMMENTS_DELETE = "comments_delete"

    LOCATIONS_READ = "locations_read"
    LOCATIONS_ADD = "locations_add"
    LOCATIONS_EDIT = "locations_edit"
    LOCATIONS_DELETE = "locations_delete"

    OBJECTS_READ = "objects_read"
    OBJECTS_ADD = "objects_add"
    OBJECTS_EDIT = "objects_edit"
    OBJECTS_DELETE = "objects_delete"

    RELATIONSHIPS_READ = "relationships_read"
    RELATIONSHIPS_ADD = "relationships_add"
    RELATIONSHIPS_EDIT = "relationships_edit"
    RELATIONSHIPS_DELETE = "relationships_delete"

    RELEASABILITY_READ = "releasability_read"
    RELEASABILITY_ADD = "releasability_add"
    RELEASABILITY_DELETE = "releasability_delete"

    SECTORS_READ = "sectors_read"
    SECTORS_EDIT = "sectors_edit"

    SERVICES_READ = "services_read"
    SERVICES_EXECUTE = "services_execute"

    SOURCES_READ = "sources_read"
    SOURCES_ADD = "sources_add"
    SOURCES_EDIT = "sources_edit"
    SOURCES_DELETE = "sources_delete"

    STATUS_READ = "status_read"
    STATUS_EDIT = "status_edit"

    TICKETS_READ = "tickets_read"
    TICKETS_ADD = "tickets_add"
    TICKETS_EDIT = "tickets_edit"
    TICKETS_DELETE = "tickets_delete"

class GeneralACL(vocab):
    """
    Vocabulary for General ACLs
    """

    API_INTERFACE = "api_interface"
    SCRIPT_INTERFACE = "script_interface"
    WEB_INTERFACE = "web_interface"

    ADD_NEW_SOURCE = "add_new_source"
    ADD_NEW_USER_ROLE = "add_new_user_role"
    ADD_NEW_TLDS = "add_new_tlds"

    CONTROL_PANEL_READ = "control_panel_read"
    CONTROL_PANEL_SYSTEM_READ = "control_panel_system_read"
    CONTROL_PANEL_GENERAL_READ = "control_panel_general_read"
    CONTROL_PANEL_GENERAL_EDIT = "control_panel_general_edit"
    CONTROL_PANEL_CRIPTS_READ = "control_panel_cripts_read"
    CONTROL_PANEL_CRIPTS_EDIT = "control_panel_cripts_edit"
    CONTROL_PANEL_LDAP_READ = "control_panel_ldap_read"
    CONTROL_PANEL_LDAP_EDIT = "control_panel_ldap_edit"
    CONTROL_PANEL_SECURITY_READ = "control_panel_security_read"
    CONTROL_PANEL_SECURITY_EDIT = "control_panel_security_edit"
    CONTROL_PANEL_DOWNLOADING_READ = "control_panel_downloading_read"
    CONTROL_PANEL_DOWNLOADING_EDIT = "control_panel_downloading_edit"
    CONTROL_PANEL_SYSTEM_SERVICES_READ = "control_panel_system_services_read"
    CONTROL_PANEL_SYSTEM_SERVICES_EDIT = "control_panel_system_services_edit"
    CONTROL_PANEL_LOGGING_READ = "control_panel_logging_read"
    CONTROL_PANEL_LOGGING_EDIT = "control_panel_logging_edit"
    CONTROL_PANEL_ITEMS_READ = "control_panel_items_read"
    CONTROL_PANEL_USERS_READ = "control_panel_users_read"
    CONTROL_PANEL_USERS_ADD = "control_panel_users_add"
    CONTROL_PANEL_USERS_EDIT = "control_panel_users_edit"
    CONTROL_PANEL_USERS_ACTIVE = "control_panel_users_active"
    CONTROL_PANEL_ROLES_READ = "control_panel_roles_read"
    CONTROL_PANEL_ROLES_EDIT = "control_panel_roles_edit"
    CONTROL_PANEL_SERVICES_READ = "control_panel_services_read"
    CONTROL_PANEL_SERVICES_EDIT = "control_panel_services_edit"
    CONTROL_PANEL_AUDIT_LOG_READ = "control_panel_audit_log_read"
    RECENT_ACTIVITY_READ = "recent_activity_read"
    STIX_IMPORT_ADD = "stix_import_add"
    DNS_TIMELINE_READ = "dns_timeline_read"
    EMAILS_TIMELINE_READ = "emails_timeline_read"

    
class DatasetACL(vocab):
    """
    Vocabulary for Dataset ACLs
    """
    DATASET = "Dataset."    
    
    NAME_EDIT = DATASET + "name_edit"
    
    # Basics
    READ = DATASET + Common.READ
    WRITE = DATASET + Common.WRITE
    DELETE = DATASET + Common.DELETE
    DOWNLOAD = DATASET + Common.DOWNLOAD
    
    SOURCES_READ = DATASET + Common.SOURCES_READ
    SOURCES_ADD = DATASET + Common.SOURCES_ADD
    SOURCES_EDIT = DATASET + Common.SOURCES_EDIT
    SOURCES_DELETE = DATASET + Common.SOURCES_DELETE

    STATUS_READ = DATASET + Common.STATUS_READ
    STATUS_EDIT = DATASET + Common.STATUS_EDIT

    TICKETS_READ = DATASET + Common.TICKETS_READ
    TICKETS_ADD = DATASET + Common.TICKETS_ADD
    TICKETS_EDIT = DATASET + Common.TICKETS_EDIT
    TICKETS_DELETE = DATASET + Common.TICKETS_DELETE
    

class EmailAddressACL(vocab):
    """
    Vocabulary for EmailAddress ACLs
    """
    EMAIL_ADDRESS = "EmailAddress."    
    
    NAME_EDIT = EMAIL_ADDRESS + "name_edit"
    
    # Basics
    READ = EMAIL_ADDRESS + Common.READ
    WRITE = EMAIL_ADDRESS + Common.WRITE
    DELETE = EMAIL_ADDRESS + Common.DELETE
    DOWNLOAD = EMAIL_ADDRESS + Common.DOWNLOAD
    
    SOURCES_READ = EMAIL_ADDRESS + Common.SOURCES_READ
    SOURCES_ADD = EMAIL_ADDRESS + Common.SOURCES_ADD
    SOURCES_EDIT = EMAIL_ADDRESS + Common.SOURCES_EDIT
    SOURCES_DELETE = EMAIL_ADDRESS + Common.SOURCES_DELETE

    STATUS_READ = EMAIL_ADDRESS + Common.STATUS_READ
    STATUS_EDIT = EMAIL_ADDRESS + Common.STATUS_EDIT

    TICKETS_READ = EMAIL_ADDRESS + Common.TICKETS_READ
    TICKETS_ADD = EMAIL_ADDRESS + Common.TICKETS_ADD
    TICKETS_EDIT = EMAIL_ADDRESS + Common.TICKETS_EDIT
    TICKETS_DELETE = EMAIL_ADDRESS + Common.TICKETS_DELETE    
    
    
class EventACL(vocab):
    """
    Vocabulary for Event ACLs
    """
    EVENT = "Event."

    ADD_SAMPLE = EVENT + "add_sample"
    TITLE_EDIT = EVENT + "title_edit"
    TYPE_EDIT = EVENT + "type_edit"

    READ = EVENT + Common.READ
    WRITE = EVENT + Common.WRITE
    DELETE = EVENT + Common.DELETE
    DOWNLOAD = EVENT + Common.DOWNLOAD

    DESCRIPTION_READ = EVENT + Common.DESCRIPTION_READ
    DESCRIPTION_EDIT = EVENT + Common.DESCRIPTION_EDIT

    ACTIONS_READ = EVENT + Common.ACTIONS_READ
    ACTIONS_ADD = EVENT + Common.ACTIONS_ADD
    ACTIONS_EDIT = EVENT + Common.ACTIONS_EDIT
    ACTIONS_DELETE = EVENT + Common.ACTIONS_DELETE

    BUCKETLIST_READ = EVENT + Common.BUCKETLIST_READ
    BUCKETLIST_EDIT = EVENT + Common.BUCKETLIST_EDIT

    COMMENTS_READ = EVENT + Common.COMMENTS_READ
    COMMENTS_ADD = EVENT + Common.COMMENTS_ADD
    COMMENTS_EDIT = EVENT + Common.COMMENTS_EDIT
    COMMENTS_DELETE = EVENT + Common.COMMENTS_DELETE

    LOCATIONS_READ = EVENT + Common.LOCATIONS_READ
    LOCATIONS_ADD = EVENT + Common.LOCATIONS_ADD
    LOCATIONS_EDIT = EVENT + Common.LOCATIONS_EDIT
    LOCATIONS_DELETE = EVENT + Common.LOCATIONS_DELETE

    OBJECTS_READ = EVENT + Common.OBJECTS_READ
    OBJECTS_ADD = EVENT + Common.OBJECTS_ADD
    OBJECTS_EDIT = EVENT + Common.OBJECTS_EDIT
    OBJECTS_DELETE = EVENT + Common.OBJECTS_DELETE

    RELATIONSHIPS_READ = EVENT + Common.RELATIONSHIPS_READ
    RELATIONSHIPS_ADD = EVENT + Common.RELATIONSHIPS_ADD
    RELATIONSHIPS_EDIT = EVENT + Common.RELATIONSHIPS_EDIT
    RELATIONSHIPS_DELETE = EVENT + Common.RELATIONSHIPS_DELETE

    RELEASABILITY_READ = EVENT + Common.RELEASABILITY_READ
    RELEASABILITY_ADD = EVENT + Common.RELEASABILITY_ADD
    RELEASABILITY_DELETE = EVENT + Common.RELEASABILITY_DELETE

    SECTORS_READ = EVENT + Common.SECTORS_READ
    SECTORS_EDIT = EVENT + Common.SECTORS_EDIT

    SERVICES_READ = EVENT + Common.SERVICES_READ
    SERVICES_EXECUTE = EVENT + Common.SERVICES_EXECUTE

    SOURCES_READ = EVENT + Common.SOURCES_READ
    SOURCES_ADD = EVENT + Common.SOURCES_ADD
    SOURCES_EDIT = EVENT + Common.SOURCES_EDIT
    SOURCES_DELETE = EVENT + Common.SOURCES_DELETE

    STATUS_READ = EVENT + Common.STATUS_READ
    STATUS_EDIT = EVENT + Common.STATUS_EDIT

    TICKETS_READ = EVENT + Common.TICKETS_READ
    TICKETS_ADD = EVENT + Common.TICKETS_ADD
    TICKETS_EDIT = EVENT + Common.TICKETS_EDIT
    TICKETS_DELETE = EVENT + Common.TICKETS_DELETE

    
class HashACL(vocab):
    """
    Vocabulary for Hash ACLs
    """
    HASH = "Hash."    
    
    NAME_EDIT = HASH + "name_edit"
    
    # Basics
    READ = HASH + Common.READ
    WRITE = HASH + Common.WRITE
    DELETE = HASH + Common.DELETE
    DOWNLOAD = HASH + Common.DOWNLOAD
    
    SOURCES_READ = HASH + Common.SOURCES_READ
    SOURCES_ADD = HASH + Common.SOURCES_ADD
    SOURCES_EDIT = HASH + Common.SOURCES_EDIT
    SOURCES_DELETE = HASH + Common.SOURCES_DELETE

    STATUS_READ = HASH + Common.STATUS_READ
    STATUS_EDIT = HASH + Common.STATUS_EDIT

    TICKETS_READ = HASH + Common.TICKETS_READ
    TICKETS_ADD = HASH + Common.TICKETS_ADD
    TICKETS_EDIT = HASH + Common.TICKETS_EDIT
    TICKETS_DELETE = HASH + Common.TICKETS_DELETE    
    
    
class TargetACL(vocab):
    """
    Vocabulary for Target ACLs
    """
    TARGET = "Target."    
    
    NAME_EDIT = TARGET + "name_edit"
    
    # Basics
    READ = TARGET + Common.READ
    WRITE = TARGET + Common.WRITE
    DELETE = TARGET + Common.DELETE
    DOWNLOAD = TARGET + Common.DOWNLOAD
    
    SOURCES_READ = TARGET + Common.SOURCES_READ
    SOURCES_ADD = TARGET + Common.SOURCES_ADD
    SOURCES_EDIT = TARGET + Common.SOURCES_EDIT
    SOURCES_DELETE = TARGET + Common.SOURCES_DELETE

    STATUS_READ = TARGET + Common.STATUS_READ
    STATUS_EDIT = TARGET + Common.STATUS_EDIT

    TICKETS_READ = TARGET + Common.TICKETS_READ
    TICKETS_ADD = TARGET + Common.TICKETS_ADD
    TICKETS_EDIT = TARGET + Common.TICKETS_EDIT
    TICKETS_DELETE = TARGET + Common.TICKETS_DELETE
    

class UserNameACL(vocab):
    """
    Vocabulary for Target ACLs
    """
    USERNAME = "Username."    
    
    NAME_EDIT = USERNAME + "name_edit"
    
    # Basics
    READ = USERNAME + Common.READ
    WRITE = USERNAME + Common.WRITE
    DELETE = USERNAME + Common.DELETE
    DOWNLOAD = USERNAME + Common.DOWNLOAD
    
    SOURCES_READ = USERNAME + Common.SOURCES_READ
    SOURCES_ADD = USERNAME + Common.SOURCES_ADD
    SOURCES_EDIT = USERNAME + Common.SOURCES_EDIT
    SOURCES_DELETE = USERNAME + Common.SOURCES_DELETE

    STATUS_READ = USERNAME + Common.STATUS_READ
    STATUS_EDIT = USERNAME + Common.STATUS_EDIT

    TICKETS_READ = USERNAME + Common.TICKETS_READ
    TICKETS_ADD = USERNAME + Common.TICKETS_ADD
    TICKETS_EDIT = USERNAME + Common.TICKETS_EDIT
    TICKETS_DELETE = USERNAME + Common.TICKETS_DELETE
    

class ReadACL(vocab):
    """
    This is to pass into base.html to see the current status of all of the
    TLOs that we want to read
    """
    ADD_NEW_SOURCE = GeneralACL.ADD_NEW_SOURCE
    ADD_NEW_USER_ROLE = GeneralACL.ADD_NEW_USER_ROLE
    ADD_NEW_TLDS = GeneralACL.ADD_NEW_TLDS

    CONTROL_PANEL_SERVICES_READ = GeneralACL.CONTROL_PANEL_SERVICES_READ
    DATASET_READ = DatasetACL.READ
    DATASET_WRITE = DatasetACL.WRITE
    EMAIL_ADDRESS_READ  = EmailAddressACL.READ
    EMAIL_ADDRESS_WRITE = EmailAddressACL.WRITE
    EVENT_READ = EventACL.READ
    EVENT_WRITE = EventACL.WRITE
    HASH_READ = HashACL.READ
    HASH_WRITE = HashACL.WRITE
    TARGET_READ = TargetACL.READ
    TARGET_WRITE = TargetACL.WRITE
    USERNAME_READ = UserNameACL.READ
    USERNAME_WRITE = UserNameACL.WRITE
