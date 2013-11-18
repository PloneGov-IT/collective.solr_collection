# -*- coding: utf-8 -*-

from plone.indexer.decorator import indexer
from Products.CMFCore.interfaces import IContentish

@indexer(IContentish)
def ploneSite(obj, **kwargs):
    return obj.getPhysicalPath()[1]
