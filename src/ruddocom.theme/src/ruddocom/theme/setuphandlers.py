# -*- coding: utf-8 -*-
import logging

from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


logger = logging.getLogger("ruddocom.theme")
logger = logger.warning


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'ruddocom.theme:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def redo_registry(portal_setup):
    try:
        if portal_setup.readDataFile("ruddocom.theme.txt") is None:
            return
    except AttributeError:
        logger("Called with %s, continuing since it appears we do not need a marker file.", portal_setup)
    logger("Setting up registry properties.")
    portal_setup.runImportStepFromProfile(
        "ruddocom.theme:default", "plone.app.registry"
    )
    logger("Done setting up registry properties.")
