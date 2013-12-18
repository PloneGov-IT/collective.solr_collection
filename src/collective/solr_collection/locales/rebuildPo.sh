#!/bin/sh

DOMAIN='collective.solr_collection'

i18ndude rebuild-pot --pot ${DOMAIN}.pot --create ${DOMAIN} ..
i18ndude sync --pot ${DOMAIN}.pot ./*/LC_MESSAGES/${DOMAIN}.po