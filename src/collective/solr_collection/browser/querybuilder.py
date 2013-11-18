from plone.app.querystring.querybuilder import QueryBuilder as Base

from plone.app.contentlisting.interfaces import IContentListing
from plone.app.querystring import queryparser

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch

class QueryBuilder(Base):
    """Force the use of Solr"""

    def _makequery(self, query=None, batch=False, b_start=0, b_size=30,
                   sort_on=None, sort_order=None, limit=0, brains=False):
        """Parse the (form)query and return using multi-adapter"""
        parsedquery = queryparser.parseFormquery(
            self.context, query, sort_on, sort_order)
        if not parsedquery:
            if brains:
                return []
            else:
                return IContentListing([])

        if self.context.getField('useSolr').get(self.context):
            parsedquery['use_solr'] = True

        catalog = getToolByName(self.context, 'portal_catalog')
        if batch:
            parsedquery['b_start'] = b_start
            parsedquery['b_size'] = b_size
        elif limit:
            parsedquery['sort_limit'] = limit

        if 'path' not in parsedquery:
            parsedquery['path'] = {'query': ''}

        # The Subject field in Plone currently uses a utf-8 encoded string.
        # When a catalog query tries to compare a unicode string from the
        # parsedquery with existing utf-8 encoded string indexes unindexing
        # will fail with a UnicodeDecodeError. To prevent this from happening
        # we always encode the Subject query.
        # XXX: As soon as Plone uses unicode for all indexes, this code can
        # be removed.
        if 'Subject' in parsedquery:
            query = parsedquery['Subject']['query']
            # query can be a unicode string or a list of unicode strings.
            if isinstance(query, unicode):
                parsedquery['Subject']['query'] = query.encode("utf-8")
            elif isinstance(query, list):
                # We do not want to change the collections' own query string,
                # therefore we create a new copy of the list.
                copy_of_query = list(query)
                # Iterate over all query items and encode them if they are
                # unicode strings
                i = 0
                for item in copy_of_query:
                    if isinstance(item, unicode):
                        copy_of_query[i] = item.encode("utf-8")
                    i += 1
                parsedquery['Subject']['query'] = copy_of_query
            else:
                pass

        results = catalog(parsedquery)
        if not brains:
            results = IContentListing(results)
        if batch:
            results = Batch(results, b_size, start=b_start)
        return results
