# -*- extra stuff goes here -*-

import logging
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.solr_collection')
logger = logging.getLogger('collective.solr_collection')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
