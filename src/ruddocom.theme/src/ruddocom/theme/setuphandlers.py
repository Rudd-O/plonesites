# -*- coding: utf-8 -*-
import logging
from six import StringIO

# Unused:
# from plone.cachepurging.utils import getPathsToPurge
from Products.CMFPlone.interfaces import INonInstallable
from plone.cachepurging.interfaces import ICachePurgingSettings
from plone.cachepurging.interfaces import IPurger
from plone.cachepurging.utils import getURLsToPurge
from plone.cachepurging.utils import isCachePurgingEnabled
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
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


def purge_urls(unused_portal_setup, urls):
    if not isCachePurgingEnabled():
        logger("Not purging anything because frontend caching is not enabled.")
        return 'Caching not enabled'
    logger("Purging URLs.")
    purger = getUtility(IPurger)
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ICachePurgingSettings)
    for path in urls:
        if not settings.cachingProxies: continue
        for url in getURLsToPurge(path, settings.cachingProxies):
            status, xcache, xerror = purger.purgeSync(url)
            logger("Purged %s — Status: %s — X-Cache: %s — Error: %s", url, status, xcache, xerror)
    logger("Done purging URLs.")


def redo_registry_and_purge_certain_urls(portal_setup):
    try:
        if portal_setup.readDataFile("ruddocom.theme.txt") is None:
            return
    except AttributeError:
        logger("Called with %s, continuing since it appears we do not need a marker file.", portal_setup)
    redo_registry(portal_setup)
    purge_urls(
        portal_setup,
        [
            "//++theme++ruddocom/less/theme-compiled.css",
        ],
    )
