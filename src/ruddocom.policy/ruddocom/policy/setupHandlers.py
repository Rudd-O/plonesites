# -*- coding: utf-8 -*-

import logging

from Products.CMFCore.utils import getToolByName


default_profile = "profile-ruddocom.policy:default"
logger = logging.getLogger("ruddocom.policy")
logger = logger.warning


def only_when_I_run(func):
    def importStep(context):
        if not hasattr(context, 'readDataFile'):
            # Not your add-on
            logger("No readDataFile!")
            return
        if hasattr(context, 'readDataFile') and context.readDataFile('ruddocom.policy.txt') is None:
            # Not your add-on
            logger("Not executing %s because data file is not there", func.__name__)
            return
        logger("Data file ruddocom.policy.txt is there, executing %s", func.__name__)
        return func(context)
    importStep.__name__ = func.__name__
    return importStep


def setupCookies(context):
    logger("Setting cookie expiry time.")
    portal_url = getToolByName(context, "portal_url")
    portal = portal_url.getPortalObject()
    l = portal.acl_users.session
    l.timeout = 604800
    l.cookie_lifetime = 14
    l.secure = True
    logger("Cookie expiry time set.")


def setupRegistryProperties(portal_setup):
    logger("Setting up registry properties.")
    portal_setup.runImportStepFromProfile(
        "ruddocom.policy:default", "plone.app.registry"
    )
    logger("Done setting up registry properties.")


@only_when_I_run
def setupAll(context):
    logger("Beginning setupAll with context %s.", context)
    setupCookies(context)
    setupRegistryProperties(context)
    logger("Ended setupAll with context %s.", context)
