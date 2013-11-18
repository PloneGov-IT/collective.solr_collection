# -*- coding: utf-8 -*-

from collective.solr_collection import logger
from Products.CMFCore.utils import getToolByName

_PROPERTIES = [
    dict(name='site_public_url', type_='string', value=''),
]

def registerProperties(context):
    ptool = getToolByName(context, 'portal_properties')
    props = ptool.solr_collection
    
    for prop in _PROPERTIES:
        if not props.hasProperty(prop['name']):
            props.manage_addProperty(prop['name'], prop['value'], prop['type_'])
            logger.info("Added missing %s property" % prop['name'])

def setupVarious(context):
    if context.readDataFile('collective.solr_collection_various.txt') is None:
        return

    portal = context.getSite()
    registerProperties(portal)
