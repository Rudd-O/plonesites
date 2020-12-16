# -*- coding: utf-8 -*-

import logging

from Products.CMFCore.utils import getToolByName


default_profile = "profile-ruddocom.policy:default"
logger = logging.getLogger("ruddocom.policy")
logger = logger.warning


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


def setupAll(context):
    logger("Beginning setupAll with context %s.", context)
    setupCookies(context)
    setupRegistryProperties(context)
    logger("Ended setupAll with context %s.", context)
