# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from plone.indexer.decorator import indexer
from Products.CMFCore.interfaces import IContentish

@indexer(IContentish)
def ploneSite(obj, **kwargs):
    return obj.getPhysicalPath()[1]

@indexer(IContentish)
def publicURL(obj, **kwargs):
    ptool = getToolByName(obj, 'portal_properties')
    solr_collection_props = getattr(ptool, 'solr_collection', None)
    if solr_collection_props and solr_collection_props.site_public_url:
        portal_url = getToolByName(obj, 'portal_url')()
        return obj.absolute_url().replace(portal_url, solr_collection_props.site_public_url)
    return obj.absolute_url()
