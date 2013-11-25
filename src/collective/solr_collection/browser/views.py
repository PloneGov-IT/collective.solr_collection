# -*- coding: utf-8 -*-
from archetypes.querywidget.views import MultiSelectWidget as BaseMultiSelectWidget
# from archetypes.querywidget.views import sortable_value
from collective.solr_collection.solr import solrUniqueValuesFor


class MultiSelectWidget(BaseMultiSelectWidget):

    def getValues(self, index=None, useSolr=False):
        if not useSolr:
            useSolr = self.request.form.get('useSolr', False)
        if useSolr:
            # FIXME: could be better to override IQuerystringRegistryReader (?)
            if not index:
                index = self.request.form.get('index')
            values = None
            if index is not None:
                values = solrUniqueValuesFor(index)
            return dict((v, {'title': v}) for v in values)
        return BaseMultiSelectWidget.getValues(self, index=index)
