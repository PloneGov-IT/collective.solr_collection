from urllib import urlencode
from logging import getLogger
from time import time
from zope.component import queryUtility
from zope.component import getUtility

from collective.solr.interfaces import ISolrConnectionConfig
from collective.solr.interfaces import ISolrConnectionManager
from collective.solr.parser import SolrResponse
from collective.solr.exceptions import SolrInactiveException

logger = getLogger(__name__)


def solrUniqueValuesFor(index):
    """
    * http://wiki.apache.org/solr/TermsComponent
    """
    start = time()
    config = queryUtility(ISolrConnectionConfig)
    # search = queryUtility(ISearch)
    manager = getUtility(ISolrConnectionManager)
    # manager = search.getManager()
    manager.setSearchTimeout()
    connection = manager.getConnection()
    if connection is None:
        raise SolrInactiveException
    response = connection.doPost(
        connection.solrBase + '/terms',
        urlencode({'terms.fl': index, 'terms.limit': -1}, doseq=True),
        connection.formheaders
    )
    results = SolrResponse(response)
    response.close()
    manager.setTimeout(None)
    elapsed = (time() - start) * 1000
    slow = config.slow_query_threshold
    if slow and elapsed >= slow:
        logger.info(
            'slow query: %d/%d ms for uniqueValuesFor (%r)',
            results.responseHeader['QTime'], elapsed, index)
    terms = getattr(results, 'terms', {})
    logger.debug('terms info: %s' % terms)
    return tuple(terms.get(index, {}).keys())
