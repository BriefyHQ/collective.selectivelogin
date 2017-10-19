# -*- coding: utf-8 -*-
"""Configuration and settings for the package."""
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

import logging


PROJECTNAME = 'collective.selectivelogin'
PROFILE_ID = 'collective.selectivelogin:default'

logger = logging.getLogger(PROJECTNAME)


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Do not show on Plone's list of installable profiles."""
        return [
            'collective.selectivelogin:profile',
            'collective.selectivelogin:uninstall',
        ]
