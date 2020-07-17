# -*- coding: utf-8 -*-

import logging

from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.Transform import make_config_persistent
from Products.CMFPlone.interfaces import ILanguage
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import queryUtility


default_profile = 'profile-ruddocom.policy:default'
logger = logging.getLogger('ruddocom.policy')
logger = logger.warning


def only_when_I_run(func):
    def importStep(context):
        if not hasattr(context, 'readDataFile'):
            # Not your add-on
            logger("No readDataFile!")
        if hasattr(context, 'readDataFile') and context.readDataFile('ruddocom.policy.txt') is None:
            # Not your add-on
            logger("Not executing %s because data file is not there", func)
            return
        logger("Executing %s", func)
        return func(context)
    importStep.func_name = func.func_name
    return importStep


def installOldStyleProducts(context):
    # Keep me in sync with configure.xml, tests.py and profiles/default/metadata.xml
    # The dependencies mechanism of metadata.xml does not install
    # old-style products properly.  It registers them with the
    # "wrong" name in the quickinstaller (no Products. prefix)
    # so they do not appear as installed in the Plone add-ons view.
    # Thus, we must install them "by hand" here.
    # FIXME: we should upgrade products that have been upgraded on
    # the file system.  That is what metadata.xml does for all
    # listed products there.
    logger("Installing old-style products")
    qi = getToolByName(context.getSite(), 'portal_quickinstaller')
    products = [
        'Products.PloneFormGen',
    ]
    installed = [x['id'] for x in qi.listInstalledProducts()]
    logger("All installed: %s", ", ".join(installed))
    logger("Already installed: %s", ", ".join(set(installed) & set(products)))
    for p in products:
        if p not in installed:
            logger("Installing %s", p)
            qi.installProduct(p)
    installed = [x['id'] for x in qi.listInstalledProducts()]
    logger("Now installed: %s", ", ".join(set(installed) & set(products)))
    logger("Old-style products installed")


def setupCookies(context):
    logger("Setting cookie expiry time")
    l = context.getSite().acl_users.session
    l.timeout = 604800
    l.cookie_lifetime = 7
    l.secure = True
    logger("Cookie expiry time set")


def setupRegistryProperties(context):
    logger("Setting up registry properties")
    ps = getToolByName(context.getSite(), 'portal_setup')
    ps.runImportStepFromProfile('ruddocom.policy:default','plone.app.registry')
    logger("Done setting up registry properties")

@only_when_I_run
def setupAll(context):
    logger("Beginning setupAll with context %s", context)
    setupCookies(context)
    installOldStyleProducts(context)
    # setupLanguage(context)
    # setupLanguageSelector(context)
    setupRegistryProperties(context)
    logger("Ended setupAll with context %s", context)
