# from urllib import urlencode
from logging import getLogger
# from time import time
from zope.component import queryUtility
# from zope.component import getUtility

from collective.solr.interfaces import ISearch
# from collective.solr.interfaces import ISolrConnectionConfig
# from collective.solr.interfaces import ISolrConnectionManager
from collective.solr.mangler import optimizeQueryParameters
# from collective.solr.parser import SolrResponse
# from collective.solr.exceptions import SolrInactiveException
# from collective.solr.interfaces import IFacetTitleVocabularyFactory

logger = getLogger(__name__)


# TERMCOMPONENT IMPLEMENTATION
# def solrUniqueValuesFor(index):
#     """
#     * http://wiki.apache.org/solr/TermsComponent
#     """
#     start = time()
#     config = queryUtility(ISolrConnectionConfig)
#     # search = queryUtility(ISearch)
#     manager = getUtility(ISolrConnectionManager)
#     # manager = search.getManager()
#     manager.setSearchTimeout()
#     connection = manager.getConnection()
#     if connection is None:
#         raise SolrInactiveException
#     response = connection.doPost(
#         connection.solrBase + '/terms',
#         urlencode({'terms.fl': index, 'terms.limit': -1}, doseq=True),
#         connection.formheaders
#     )
#     results = SolrResponse(response)
#     response.close()
#     manager.setTimeout(None)
#     elapsed = (time() - start) * 1000
#     slow = config.slow_query_threshold
#     if slow and elapsed >= slow:
#         logger.info(
#             'slow query: %d/%d ms for uniqueValuesFor (%r)',
#             results.responseHeader['QTime'], elapsed, index)
#     terms = getattr(results, 'terms', {})
#     logger.debug('terms info: %s' % terms)
#     return tuple(terms.get(index, {}).keys())

# FACET IMPLEMENTAION
def solrUniqueValuesFor(index, **args):
    """
    """
    search = queryUtility(ISearch)
    params = {
        'rows': 0,
        'facet': 'true',
        'facet.field': index,
        'facet.mincount': 1,
    }
    query = search.buildQuery(**args) if args else {}
    if query != {}:
        optimizeQueryParameters(query, params)
        __traceback_info__ = (query, params, args)
    else:
        query = {'*': '*'}
        # query = {index: '*'}
    results = search(query, **params)
    terms = getattr(results, 'facet_counts', {}).get('facet_fields', {})
    # vfactory = queryUtility(IFacetTitleVocabularyFactory, name=index)
    # if vfactory is None:
    #    # Use the default fallback
    #    vfactory = getUtility(IFacetTitleVocabularyFactory)
    # vocabulary = vfactory(view.context)
    return tuple(terms.get(index, {}).keys())
