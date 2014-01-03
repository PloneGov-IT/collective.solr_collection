# -*- coding: utf-8 -*-
from zope.component import adapts
from zope.interface import implements
from collective.solr.flare import PloneFlare
from collective.solr.interfaces import IFlare, ISolrFlare
from collective.solr_collection import logger
from collective.solr_collection.interfaces import ISolrCollectionLayer


class SolrCollectionFlare(PloneFlare):
    """ a sol(a)r brain, i.e. a data container for search results """
    implements(IFlare)
    adapts(ISolrFlare, ISolrCollectionLayer)

    __allow_access_to_unprotected_subobjects__ = True

    def getURL(self, relative=False):
        """ convert the physical path into a url, if it was stored """
        path = self.getPath()
        path = path.encode('utf-8')
        public_url = getattr(self, 'publicURL', None)
        if relative:
            logger.warning('getURL called with relative for path %s' % path)
            return PloneFlare.getURL(self, relative)
        if not public_url:
            return PloneFlare.getURL(self, relative)
        return public_url
