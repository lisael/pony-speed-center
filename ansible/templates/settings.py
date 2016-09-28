# -*- coding: utf-8 -*-
# Django settings for a Codespeed project.
import os

DEBUG = {{ DEBUG }}
TEMPLATE_DEBUG = DEBUG

BASEDIR = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.split(BASEDIR)[1]

#: The directory which should contain checked out source repositories:
REPOSITORY_BASE_PATH = os.path.join(BASEDIR, "repos")

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASEDIR, 'data.db'),
    }
}

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False

MEDIA_ROOT = os.path.join(BASEDIR, "media")

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

SECRET_KEY = 'as%n_m#)^vee2pe91^^@c))sl7^c6t-9r8n)_69%)2yt+(la2&'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

if DEBUG:
    import traceback
    import logging

    # Define a class that logs unhandled errors
    class LogUncatchedErrors:
        def process_exception(self, request, exception):
            logging.error("Unhandled Exception on request for %s\n%s",
                          request.build_absolute_uri(), traceback.format_exc())
    # And add it to the middleware classes
    MIDDLEWARE_CLASSES += ('sample_project.settings.LogUncatchedErrors',)

    # set shown level of logging output to debug
    logging.basicConfig(level=logging.DEBUG)

ROOT_URLCONF = '{0}.urls'.format(TOPDIR)

TEMPLATE_DIRS = (
    os.path.join(BASEDIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'codespeed',
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASEDIR, "sitestatic")
STATICFILES_DIRS = (
    os.path.join(BASEDIR, 'static'),
)

# Codespeed settings that can be overwritten here.
from codespeed.settings import *  # noqa

## General default options ##
WEBSITE_NAME = "{{ WEBSITE_NAME }}"  # This name will be used in the reports RSS feed

DEF_ENVIRONMENT = None  # Name of the environment which should be selected as default

DEF_BRANCH = "{{ DEF_BRANCH }}"  # Defines the default branch to be used.
                                 # In git projects, this branch is usually
                                 # be calles "master"

DEF_BASELINE = None # Which executable + revision should be default as a baseline
                    # Given as the name of the executable and commitid of the revision
                    # Example: defaultbaseline = {'executable': 'myexe', 'revision': '21'}

TREND = 10 # Default value for the depth of the trend
           # Used by reports for the latest runs and changes view

# Threshold that determines when a performance change over the last result is significant
CHANGE_THRESHOLD = 3.0

# Threshold that determines when a performance change
# over a number of revisions is significant
TREND_THRESHOLD = 5.0

## Changes view options ##
DEF_EXECUTABLE = None # Executable that should be chosen as default in the changes view
                      # Given as the name of the executable.
                      # Example: defaultexecutable = "myexe"

SHOW_AUTHOR_EMAIL_ADDRESS = True # Whether to show the authors email address in the
                                 # changes log

## Timeline view options ##
DEF_BENCHMARK = None   # Default selected benchmark. Possible values:
                       #   None: will show a grid of plot thumbnails, or a
                       #       text message when the number of plots exceeds 30
                       #   "grid": will always show as default the grid of plots
                       #   "show_none": will show a text message (better
                       #       default when there are lots of benchmarks)
                       #   "mybench": will select benchmark named "mybench"

DEF_TIMELINE_LIMIT = 50  # Default number of revisions to be plotted
                         # Possible values 10,50,200,1000

#TIMELINE_BRANCHES = True # NOTE: Only the default branch is currently shown
                         # Get timeline results for specific branches
                         # Set to False if you want timeline plots and results only for trunk.

## Comparison view options ##
CHART_TYPE = 'normal bars' # The options are 'normal bars', 'stacked bars' and 'relative bars'

NORMALIZATION = False # True will enable normalization as the default selection
                      # in the Comparison view. The default normalization can be
                      # chosen in the defaultbaseline setting

CHART_ORIENTATION = 'vertical' # 'vertical' or 'horizontal can be chosen as
                              # default chart orientation

COMP_EXECUTABLES = None  # Which executable + revision should be checked as default
                         # Given as a list of tuples containing the
                         # name of an executable + commitid of a revision
                         # An 'L' denotes the last revision
                         # Example:
                         # COMP_EXECUTABLES = [
                         #     ('myexe', '21df2423ra'),
                         #     ('myexe', 'L'),]

USE_MEDIAN_BANDS = True # True to enable median bands on Timeline view

