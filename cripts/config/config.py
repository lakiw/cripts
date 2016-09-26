import os

from mongoengine import Document, StringField, ListField
from mongoengine import BooleanField, IntField

from cripts.core.cripts_mongoengine import CriptsDocument

class CRIPTsConfig(CriptsDocument, Document):
    """
    CRIPTs Configuration Class.
    """
    
    from django.conf import settings

    meta = {
        "collection": settings.COL_CONFIG,
        "cripts_type": 'Config',
        "latest_schema_version": 1,
        "schema_doc": {
        },
    }
    allowed_hosts = ListField(StringField(), default=['*'])
    classification = StringField(default='unclassified')
    company_name = StringField(default='My Company')
    create_unknown_user = BooleanField(default=False)
    cripts_message = StringField(default='')
    cripts_email = StringField(default='')
    cripts_email_subject_tag = StringField(default='')
    cripts_email_end_tag = BooleanField(default=True)
    # This is actually the internal DB version, but is named cripts_version
    # for historical reasons.
    cripts_version = StringField(required=True,
                                default=settings.CRIPTS_VERSION)
    debug = BooleanField(default=True)
    depth_max = IntField(default=10)
    email_host = StringField(default='')
    email_port = StringField(default='')
    enable_api = BooleanField(default=False)
    enable_toasts = BooleanField(default=False)
    git_repo_url = StringField(default='https://github.com/lakiw/cripts')
    http_proxy = StringField(default='')
    instance_name = StringField(default='My Instance')
    instance_url = StringField(default='')
    invalid_login_attempts = IntField(default=3)
    language_code = StringField(default='en-us')
    ldap_auth = BooleanField(default=False)
    ldap_tls = BooleanField(default=False)
    ldap_server = StringField(default='')
    ldap_bind_dn = StringField(default='')
    ldap_bind_password = StringField(default='')
    ldap_usercn = StringField(default='')
    ldap_userdn = StringField(default='')
    ldap_update_on_login = BooleanField(default=False)
    log_directory = StringField(default=os.path.join(settings.SITE_ROOT, '..', 'logs'))
    log_level = StringField(default='INFO')
    password_complexity_desc = StringField(default='No complexity requriement')
    password_complexity_regex = StringField(default='')
    query_caching = BooleanField(default=False)
    rel_max = IntField(default=50)
    remote_user = BooleanField(default=False)
    rt_url = StringField(default='')
    secure_cookie = BooleanField(default=True)
    service_dirs = ListField(StringField())
    service_model = StringField(default='process')
    service_pool_size = IntField(default=12)
    session_timeout = IntField(default=12)
    splunk_search_url = StringField(default='')
    temp_dir = StringField(default='/tmp')
    timezone = StringField(default='America/New_York')
    total_max = IntField(default=250)
    totp_web = StringField(default='Disabled')
    totp_cli = StringField(default='Disabled')
    zip7_path = StringField(default='/usr/bin/7z')
    zip7_password = StringField(default='hashes')
    
    print "END"

    def migrate(self):
        """
        Migrate the Configuration Schema to the latest version.
        """

        pass
