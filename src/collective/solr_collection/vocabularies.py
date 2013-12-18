# -*- coding: utf-8 -*-
from binascii import b2a_qp
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from collective.solr_collection.solr import solrUniqueValuesFor


class PloneSiteVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = [SimpleTerm(i, i, i)
                 for i in solrUniqueValuesFor('ploneSite')]
        return SimpleVocabulary(items)

PloneSiteVocabularyFactory = PloneSiteVocabulary()
