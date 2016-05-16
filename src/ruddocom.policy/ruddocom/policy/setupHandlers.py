# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.Transform import make_config_persistent
from Products.CMFPlone.interfaces import ILanguage


def createContent(context):
    logger = context.getLogger('ruddocom.policy')
    logger.info("Creating content")
    l = context.getSite()
    if "en" not in l:
        l.invokeFactory("Folder", "en")
    if "es" not in l:
        l.invokeFactory("Folder", "es")
    l['en'].setTitle(u"Rudd-O.com in English")
    l['es'].setTitle(u"Rudd-O.com en español")
    l['en'].setDescription(u"Linux, free software, voluntaryism and cypherpunk.  Established 1999.")
    l['es'].setDescription(u"Linux, software libre, voluntarismo y cypherpunk.  Desde 1999.")
    ILanguage(l['en']).set_language('en')
    ILanguage(l['es']).set_language('es')
    logger.info("Content created")

def setupCookies(context):
    logger = context.getLogger('ruddocom.policy')
    logger.info("Setting cookie expiry time")
    l = context.getSite().acl_users.session
    l.timeout = 604800
    l.cookie_lifetime = 7
    l.secure = True
    logger.info("Cookie expiry time set")

def setupAll(context):
    logger = context.getLogger('ruddocom.policy')
    logger.info("Beginning setupAll with context %s", context)
    datafile = context.readDataFile('ruddocom.policy.txt') if hasattr(context, 'readDataFile') else None
    if datafile is None:
        # Not your add-on
        return
    setupCookies(context)
    createContent(context)
