# -*- coding: utf-8 -*-

from archetypes.querywidget.views import MultiSelectWidget as BaseMultiSelectWidget

class MultiSelectWidget(BaseMultiSelectWidget):

    def getValues(self, index=None, useSolr=False):
        if not useSolr:
            useSolr = self.request.form.get('useSolr', False)
        if useSolr:
            # TODO: we must use solr if we get "user_solr" in the request
            pass
        return BaseMultiSelectWidget.getValues(self, index=index)
