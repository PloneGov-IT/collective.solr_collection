# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements
from .interfaces import ISolrCollectionLayer
from Products.Archetypes import atapi
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender, IOrderableSchemaExtender
from plone.app.collection.interfaces import ICollection
from collective.solr_collection import _
from archetypes.schemaextender.field import ExtensionField
from plone.app.collection import PloneMessageFactory as pmf
from archetypes.querywidget.field import QueryField
from archetypes.querywidget.widget import QueryWidget


class ExtensionBooleanField(ExtensionField, atapi.BooleanField):
    """ derivative of boolean for extending schemas """

class ExtensionQueryField(ExtensionField, QueryField):
    """ derivative of queryfield for extending schemas """


class SolrCollectionExtender(object):
    adapts(ICollection)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)

    layer = ISolrCollectionLayer

    fields = [

        ExtensionQueryField(
            name='query',
            widget=QueryWidget(
                label=pmf(u"Search terms"),
                description=pmf(u"Define the search terms for the items you want to "
                                u"list by choosing what to match on. "
                                u"The list of results will be dynamically updated."),
                helper_js = ('++resource++archetypes.querywidget.querywidget.js',
                             '@@datepickerconfig',
                             '++resource++collective.solr_collection.js'),
                ),
            validators=('javascriptDisabled',)
        ),

        ExtensionBooleanField('useSolr',
            default=False,
            languageIndependent=True,
            widget=atapi.BooleanWidget(
                label=_(u"Use Solr"),
                description=_('help_use_solr',
                              default=u"When checked, query Solr instead of site catalog"),
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, original):
        index = original['default'].index('query')
        fieldName = original['default'].pop()
        original['default'].insert(index, fieldName)
        return original
