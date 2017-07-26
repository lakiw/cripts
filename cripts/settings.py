# CRIPTs environment chooser

import errno
import glob
import os
import sys
import django
import subprocess

from pymongo import ReadPreference, MongoClient
from mongoengine import connect
from mongoengine import __version__ as mongoengine_version
from pymongo import version as pymongo_version

from distutils.version import StrictVersion

sys.path.insert(0, os.path.dirname(__file__))

# calculated paths for django and the site
# used as starting points for various other paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
# Version
CRIPTS_VERSION = '1-master'

#the following gets the current git hash to be displayed in the footer and
#hides it if it is not a git repo
try:
    HIDE_GIT_HASH = False
    #get the short hand of current git hash
    GIT_HASH = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=SITE_ROOT).strip()
    #get the long hand of the current git hash
    GIT_HASH_LONG = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=SITE_ROOT).strip()
    #get the git branch
    GIT_BRANCH = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=SITE_ROOT).strip()
except:
    #if it is not a git repo, clear out all values and hide them
    GIT_HASH = ''
    GIT_HASH_LONG = ''
    HIDE_GIT_HASH = True
    GIT_BRANCH = ''

APPEND_SLASH = True
TEST_RUN = False

# Get Django version
django_version = django.get_version()

#Check mongoengine version (we got it from import)
if StrictVersion(mongoengine_version) < StrictVersion('0.10.0'):
    old_mongoengine = True
    #raise Exception("Mongoengine versions prior to 0.10 are no longer supported! Please see UPDATING!")
else:
    old_mongoengine = False

# Set to DENY|SAMEORIGIN|ALLOW-FROM uri
# Default: SAMEORIGIN
# More details: https://developer.mozilla.org/en-US/docs/HTTP/X-Frame-Options
#X_FRAME_OPTIONS = 'ALLOW-FROM https://www.example.com'

# Setup for runserver or Apache
if 'runserver' in sys.argv:
    DEVEL_INSTANCE = True
    SERVICE_MODEL = 'thread'
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    LOGIN_URL = "/login/"
elif 'test' in sys.argv:
    TEST_RUN = True
    DEVEL_INSTANCE = True
    SERVICE_MODEL = 'thread'
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    LOGIN_URL = "/login/"
else:
    DEVEL_INSTANCE = False
    SERVICE_MODEL = 'process'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    LOGIN_URL = "/login/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy'
    }
}


# MongoDB Default Configuration
# Tip: To change database settings, override by using
#      template from config/database_example.py
MONGO_HOST = 'localhost'                          # server to connect to
MONGO_PORT = 27017                                # port MongoD is running on
MONGO_DATABASE = 'cripts'                          # database name to connect to
MONGO_SSL = False                                 # whether MongoD has SSL enabled
MONGO_USER = ''                                   # username used to authenticate to mongo (normally empty)
MONGO_PASSWORD = ''                               # password for the mongo user
MONGO_REPLICASET = None                           # Name of RS, if mongod in replicaset

# File storage backends
S3 = "S3"
GRIDFS = "GRIDFS"

# DB to use for files
FILE_DB = GRIDFS

# S3 buckets
BUCKET_OBJECTS = "objects"

# Import custom Database config
dbfile = os.path.join(SITE_ROOT, 'config/database.py')
if os.path.exists(dbfile):
    execfile(dbfile)

if TEST_RUN:
    MONGO_DATABASE = 'cripts-unittest'

# Read preference to configure which nodes you can read from
# Possible values:
# primary: queries are sent to the primary node in a replicSet
# secondary: queries are allowed if sent to primary or secondary
#            (for single host) or are distributed to secondaries
#            if you are connecting through a router
# More info can be found here:
# http://api.mongodb.org/python/current/api/pymongo/index.html
MONGO_READ_PREFERENCE = ReadPreference.PRIMARY


# MongoDB default collections
COL_ANALYSIS_RESULTS = "analysis_results"                 # analysis results
COL_AUDIT_LOG = "audit_log"                               # audit log entries
COL_BUCKET_LISTS = "bucket_lists"                         # bucketlist information
COL_COMMENTS = "comments"                                 # comments collection
COL_CONFIG = "config"                                     # config collection
COL_COUNTS = "counts"                                     # general counts for dashboard
COL_DATASETS = "datasets"                                 # Holds a password dataset
COL_EMAIL_ADDRESSES = "email_addresses"                   # An email address found in a dataset
COL_EVENTS = "events"                                     # main events collection
COL_EVENT_TYPES = "event_types"                           # event types for events
COL_HASHES = "hashes"                                     # password hashes
COL_HASH_STATS ="hash_stats"                              # statistics about the individual hash types
COL_IDB_ACTIONS = "idb_actions"                           # list of available actions to be taken with indicators
COL_LOCATIONS = "locations"                               # Locations collection
COL_NOTIFICATIONS = "notifications"                       # notifications collection
COL_OBJECTS = "objects"                                   # objects that are files that have been added
COL_OBJECT_TYPES = "object_types"                         # types of objects that can be added
COL_RELATIONSHIP_TYPES = "relationship_types"             # list of available relationship types
COL_ROLES = "roles"                                       # main roles collection
COL_SECTOR_LISTS = "sector_lists"                         # sector lists information
COL_SECTORS = "sectors"                                   # available sectors
COL_SERVICES = "services"                                 # list of services for scanning
COL_SOURCE_ACCESS = "source_access"                       # source access ACL collection
COL_SOURCES = "sources"                                   # source information generated by MapReduce
COL_STATISTICS = "statistics"                             # list of statistics for different objects (campaigns, for example)
COL_TARGETS = "targets"                                   # targets that campaings are going against
COL_USERNAMES = "usernames"                               # usernames associated with hashes
COL_USERS = "users"                                       # main users collection

# MongoDB connection pool
if MONGO_USER:
    connect(MONGO_DATABASE, host=MONGO_HOST, port=MONGO_PORT, read_preference=MONGO_READ_PREFERENCE, ssl=MONGO_SSL,
            replicaset=MONGO_REPLICASET, username=MONGO_USER, password=MONGO_PASSWORD)
else:
    connect(MONGO_DATABASE, host=MONGO_HOST, port=MONGO_PORT, read_preference=MONGO_READ_PREFERENCE, ssl=MONGO_SSL,
            replicaset=MONGO_REPLICASET)

# Get config from DB
c = MongoClient(MONGO_HOST, MONGO_PORT, ssl=MONGO_SSL)
db = c[MONGO_DATABASE]
if MONGO_USER:
    db.authenticate(MONGO_USER, MONGO_PASSWORD)
coll = db[COL_CONFIG]
cripts_config = coll.find_one({})
if not cripts_config:
    cripts_config = {}

# UberAdmin role. Has access to everything, can do everything, etc.
ADMIN_ROLE = "UberAdmin"

# Populate settings
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
# NOTE: we are setting ALLOWED_HOSTS to ['*'] by default which will work
#       everywhere but is insecure for production installations (no less secure
#       than setting DEBUG to True). This is done because we can't anticipate
#       the host header for every CRIPTs install and this should work "out of
#       the box".
ALLOWED_HOSTS =             cripts_config.get('allowed_hosts', ['*'])
COMPANY_NAME =              cripts_config.get('company_name', 'My Company')
CLASSIFICATION =            cripts_config.get('classification', 'unclassified')
CRIPTS_EMAIL =              cripts_config.get('cripts_email', '')
CRIPTS_EMAIL_SUBJECT_TAG =  cripts_config.get('cripts_email_subject_tag', '')
CRIPTS_EMAIL_END_TAG =      cripts_config.get('cripts_email_end_tag', True)
DEBUG =                     cripts_config.get('debug', True)
if cripts_config.get('email_host', None):
    EMAIL_HOST =            cripts_config.get('email_host', None)
if cripts_config.get('email_port', None):
    EMAIL_PORT =        int(cripts_config.get('email_port', None))
ENABLE_API =                cripts_config.get('enable_api', False)
ENABLE_TOASTS =             cripts_config.get('enable_toasts', False)
GIT_REPO_URL =              cripts_config.get('git_repo_url', '')
HTTP_PROXY =                cripts_config.get('http_proxy', None)
INSTANCE_NAME =             cripts_config.get('instance_name', 'My Instance')
INSTANCE_URL =              cripts_config.get('instance_url', '')
INVALID_LOGIN_ATTEMPTS =    cripts_config.get('invalid_login_attempts', 3) - 1
LANGUAGE_CODE =             cripts_config.get('language_code', 'en-us')
LDAP_AUTH =                 cripts_config.get('ldap_auth', False)
LDAP_SERVER =               cripts_config.get('ldap_server', '')
LDAP_BIND_DN =              cripts_config.get('ldap_bind_dn', '')
LDAP_BIND_PASSWORD =        cripts_config.get('ldap_bind_password', '')
LDAP_USERDN =               cripts_config.get('ldap_userdn', '')
LDAP_USERCN =               cripts_config.get('ldap_usercn', '')
LOG_DIRECTORY =             cripts_config.get('log_directory', os.path.join(SITE_ROOT, '..', 'logs'))
LOG_LEVEL =                 cripts_config.get('log_level', 'INFO')
QUERY_CACHING =             cripts_config.get('query_caching', False)
RT_URL =                    cripts_config.get('rt_url', None)
SECURE_COOKIE =             cripts_config.get('secure_cookie', True)
SERVICE_DIRS =        tuple(cripts_config.get('service_dirs', []))
SERVICE_MODEL =             cripts_config.get('service_model', SERVICE_MODEL)
SERVICE_POOL_SIZE =     int(cripts_config.get('service_pool_size', 12))
SESSION_TIMEOUT =       int(cripts_config.get('session_timeout', 12)) * 60 * 60
SPLUNK_SEARCH_URL =         cripts_config.get('splunk_search_url', None)
TEMP_DIR =                  cripts_config.get('temp_dir', '/tmp')
TIME_ZONE =                 cripts_config.get('timezone', 'America/New_York')
ZIP7_PATH =                 cripts_config.get('zip7_path', '/usr/bin/7z')
ZIP7_PASSWORD =             cripts_config.get('zip7_password', 'hashed')
REMOTE_USER =               cripts_config.get('remote_user', False)
PASSWORD_COMPLEXITY_REGEX = cripts_config.get('password_complexity_regex', '')
PASSWORD_COMPLEXITY_DESC =  cripts_config.get('password_complexity_desc', 'No complexity requirement. This is a password hash research platform. I trust you to do what you need to.')
DEPTH_MAX =                 cripts_config.get('depth_max', '10')
TOTAL_MAX =                 cripts_config.get('total_max', '250')
REL_MAX =                   cripts_config.get('rel_max', '50')
TOTP =                      cripts_config.get('totp', False)


COLLECTION_TO_BUCKET_MAPPING = {
    COL_OBJECTS: BUCKET_OBJECTS,
}

# check Log Directory
if not os.path.exists(LOG_DIRECTORY):
    LOG_DIRECTORY = os.path.join(SITE_ROOT, '..', 'logs')

# Custom settings for Django
_TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# DATE and DATETIME Formats
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s.u'
PY_DATE_FORMAT = '%Y-%m-%d'
PY_TIME_FORMAT = '%H:%M:%S.%f'
PY_DATETIME_FORMAT = ' '.join([PY_DATE_FORMAT, PY_TIME_FORMAT])
OLD_PY_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
PY_FORM_DATETIME_FORMATS = [PY_DATETIME_FORMAT, OLD_PY_DATETIME_FORMAT]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SITE_ROOT, '../extras/www')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/'

STATIC_ROOT = os.path.join(SITE_ROOT, '../extras/www/static')
STATIC_URL = '/static/'

# List of callables that know how to import templates from various sources.
#https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
_TEMPLATE_LOADERS = [
    ('django.template.loaders.cached.Loader', [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.load_template_source',
    ])
]

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': 'unix:/data/memcached.sock',
#    }
#}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

_TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'cripts.core.views.base_context',
    'cripts.core.views.collections',
    'cripts.core.views.user_context',
]

ROOT_URLCONF = 'cripts.urls'

_TEMPLATE_DIRS = [
    os.path.join(SITE_ROOT, '../documentation'),
    os.path.join(SITE_ROOT, 'core/templates'),
    os.path.join(SITE_ROOT, 'core/dashboard/templates'),
    os.path.join(SITE_ROOT, 'comments/templates'),
    os.path.join(SITE_ROOT, 'config/templates'),
    os.path.join(SITE_ROOT, 'datasets/templates'),
    os.path.join(SITE_ROOT, 'email_addresses/templates'),
    os.path.join(SITE_ROOT, 'events/templates'),
    os.path.join(SITE_ROOT, 'hashes/templates'),
    os.path.join(SITE_ROOT, 'hash_types/templates'),
    os.path.join(SITE_ROOT, 'objects/templates'),
    os.path.join(SITE_ROOT, 'relationships/templates'),
    os.path.join(SITE_ROOT, 'services/templates'),
    os.path.join(SITE_ROOT, 'stats/templates'),
    os.path.join(SITE_ROOT, 'targets/templates'),
    os.path.join(SITE_ROOT, 'usernames/templates'),
    os.path.join(SITE_ROOT, 'core/templates/dialogs'),
    os.path.join(SITE_ROOT, 'comments/templates/dialogs'),
    os.path.join(SITE_ROOT, 'objects/templates/dialogs'),
    os.path.join(SITE_ROOT, 'relationships/templates/dialogs'),

]


STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'core/static'),
    os.path.join(SITE_ROOT, 'dashboards/static'),
    os.path.join(SITE_ROOT, 'comments/static'),
    os.path.join(SITE_ROOT, 'objects/static'),
    os.path.join(SITE_ROOT, 'relationships/static'),
    os.path.join(SITE_ROOT, 'services/static'),
    os.path.join(SITE_ROOT, 'config/static'),
)


AUTH_USER_MODEL = 'mongo_auth.MongoUser'
MONGOENGINE_USER_DOCUMENT = 'cripts.core.user.CRIPTsUser'

# http://django-debug-toolbar.readthedocs.org/en/latest/configuration.html#debug-toolbar-panels
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'vcs_info_panel.panels.GitInfoPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
    'template_profiler_panel.panels.template.TemplateProfilerPanel',
    'debug_toolbar_mongo.panel.MongoDebugPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.sql.SQLPanel',
]
INTERNAL_IPS = '127.0.0.1'

if old_mongoengine:
    INSTALLED_APPS = (
        'cripts.core',
        'cripts.dashboards',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.messages',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.staticfiles',
        'cripts.datasets',
        'cripts.email_addresses',
        'cripts.events',
        'cripts.hashes',
        'cripts.objects', 
        'cripts.relationships',
        'cripts.services',
        'cripts.stats',
        'cripts.targets',
        'cripts.usernames',
        'tastypie',
        'tastypie_mongoengine',
        'mongoengine.django.mongo_auth',
        'template_timings_panel',
        'template_profiler_panel',
        'debug_toolbar_mongo',
        'vcs_info_panel',
        'debug_toolbar',
    )

    MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cripts.core.exceptions.ErrorMiddleware',
    # Only needed for mongoengine<0.10
    'cripts.core.user.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    SESSION_ENGINE = 'mongoengine.django.sessions'

    SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'

    AUTHENTICATION_BACKENDS = (
        'cripts.core.user.CRIPTsAuthBackend',
    )

else:
    INSTALLED_APPS = (
        'cripts.core',
        'cripts.dashboards',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.messages',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.staticfiles',
        'cripts.datasets',
        'cripts.email_addresses',
        'cripts.events',
        'cripts.hashes',
        'cripts.objects',
        'cripts.relationships',
        'cripts.services',
        'cripts.stats',
        'cripts.targets',
        'cripts.usernames',
        'tastypie',
        'tastypie_mongoengine',
        'django_mongoengine',
        'django_mongoengine.mongo_auth',
        'template_timings_panel',
        'template_profiler_panel',
        'debug_toolbar_mongo',
        'vcs_info_panel',
        'debug_toolbar',
        )

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'cripts.core.exceptions.ErrorMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    SESSION_ENGINE = 'django_mongoengine.sessions'

    SESSION_SERIALIZER = 'django_mongoengine.sessions.BSONSerializer'

    AUTHENTICATION_BACKENDS = (
        #'django_mongoengine.mongo_auth.backends.MongoEngineBackend',
        'cripts.core.user.CRIPTsAuthBackend',
    )

if REMOTE_USER:
    AUTHENTICATION_BACKENDS = (
        'cripts.core.user.CRIPTsRemoteUserBackend',
    )
    if old_mongoengine:
        MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'cripts.core.user.AuthenticationMiddleware',
            'django.contrib.auth.middleware.RemoteUserMiddleware',
            'cripts.core.exceptions.ErrorMiddleware',
            'debug_toolbar.middleware.DebugToolbarMiddleware',
        )
    else:
        MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.RemoteUserMiddleware',
            'cripts.core.exceptions.ErrorMiddleware',
            'debug_toolbar.middleware.DebugToolbarMiddleware',
        )

MONGODB_DATABASES = {
    "default": {
        "name": 'cripts',
        "host": '127.0.0.1',
        "password": None,
        "username": None,
        "tz_aware": True, # if you using timezones in django (USE_TZ = True)
    },
}

# Handle logging after all custom configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "%(levelname)s %(asctime)s %(name)s %(message)s"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'normal': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIRECTORY, 'cripts.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'cripts': {
            'handlers': ['normal'],
            'propagate': True,
            'level': 'DEBUG',
        },
    },
}

# Handle creating log directories if they do not exist
for handler in LOGGING['handlers'].values():
    log_file = handler.get('filename')
    if log_file:
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)

            except OSError as e:
                # If file exists
                if e.args[0] == errno.EEXIST:
                    pass
                # re-raise on error that is not
                # easy to automatically handle, such
                # as permission errors
                else:
                    raise

# CRIPTs Types
CRIPTS_TYPES = {
    'AnalysisResult': COL_ANALYSIS_RESULTS,
    'Comment': COL_COMMENTS,
    'Dataset': COL_DATASETS,
    'EmailAddress': COL_EMAIL_ADDRESSES,
    'Event': COL_EVENTS,
    'Hash': COL_HASHES,
    'Target': COL_TARGETS,
    'UserName': COL_USERNAMES,
    'Notification': COL_NOTIFICATIONS,
}


# Custom template lists for loading in different places in the UI
SERVICE_NAV_TEMPLATES = ()
SERVICE_CP_TEMPLATES = ()
SERVICE_TAB_TEMPLATES = ()

# discover services
for service_directory in SERVICE_DIRS:
    if os.path.isdir(service_directory):
        sys.path.insert(0, service_directory)
        for d in os.listdir(service_directory):
            abs_path = os.path.join(service_directory, d, 'templates')
            if os.path.isdir(abs_path):
                _TEMPLATE_DIRS += (abs_path,)
                nav_items = os.path.join(abs_path, '%s_nav_items.html' % d)
                cp_items = os.path.join(abs_path, '%s_cp_items.html' % d)
                view_items = os.path.join(service_directory, d, 'views.py')
                if os.path.isfile(nav_items):
                    SERVICE_NAV_TEMPLATES = SERVICE_NAV_TEMPLATES + ('%s_nav_items.html' % d,)
                if os.path.isfile(cp_items):
                    SERVICE_CP_TEMPLATES = SERVICE_CP_TEMPLATES + ('%s_cp_items.html' % d,)
                if os.path.isfile(view_items):
                    if '%s_context' % d in open(view_items).read():
                        context_module = '%s.views.%s_context' % (d, d)
                        _TEMPLATE_CONTEXT_PROCESSORS += (context_module,)
                for tab_temp in glob.glob('%s/*_tab.html' % abs_path):
                    head, tail = os.path.split(tab_temp)
                    ctype = tail.split('_')[-2]
                    name = "_".join(tail.split('_')[:-2])
                    SERVICE_TAB_TEMPLATES = SERVICE_TAB_TEMPLATES + ((ctype, name, tail),)

# Allow configuration of the META or HEADER variable is used to find
# remote username when REMOTE_USER is enabled.
REMOTE_USER_META = 'REMOTE_USER'

# The next example could be used for reverse proxy setups
# where your frontend might pass Remote-User: header.
#
# WARNING: If you enable this, be 100% certain your backend is not
# directly accessible and this header could be spoofed by an attacker.
#
# REMOTE_USER_META = 'HTTP_REMOTE_USER'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'APP_DIRS': False,'
        'DIRS': _TEMPLATE_DIRS,

        'OPTIONS': {

            #'dirs' : #_TEMPLATE_DIRS,
            'context_processors' : _TEMPLATE_CONTEXT_PROCESSORS,
            'debug' : _TEMPLATE_DEBUG,
            'loaders' : _TEMPLATE_LOADERS,

        },
    },
]

if StrictVersion(django_version) < StrictVersion('1.8.0'):
    TEMPLATE_DEBUG = _TEMPLATE_DEBUG
    TEMPLATE_DIRS = _TEMPLATE_DIRS
    TEMPLATE_CONTEXT_PROCESSORS = _TEMPLATE_CONTEXT_PROCESSORS

# Import custom settings if it exists
csfile = os.path.join(SITE_ROOT, 'config/overrides.py')
if os.path.exists(csfile):
    execfile(csfile)
