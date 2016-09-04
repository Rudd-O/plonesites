# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.Transform import make_config_persistent
from Products.CMFPlone.interfaces import ILanguage

default_profile = 'profile-ruddocom.policy:default'
logger = context.getLogger('ruddocom.policy')

def only_when_I_run(func):
    def importStep(context):
        logger.info("Checking whether I get to run")
        if not hasattr(context, 'readDataFile'):
            logger.info("No readDataFile in context")
            # Not your add-on
            return
        if context.readDataFile('ruddocom.policy.txt') is None:
            logger.info("Nothing in file ruddocom.policy.txt")
            # Not your add-on
            return
        logger.info("Executing %s", func)
        return func(context)
    importStep.func_name = func.func_name
    return importStep


def createContent(context):
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
    logger.info("Setting cookie expiry time")
    l = context.getSite().acl_users.session
    l.timeout = 604800
    l.cookie_lifetime = 7
    l.secure = True
    logger.info("Cookie expiry time set")

@only_when_I_run
def setupAll(context):
    logger.info("Beginning setupAll with context %s", context)
    setupCookies(context)
    createContent(context)
    logger.info("Ended setupAll with context %s", context)

@only_when_I_run
def upgradeContent(context):
    ps = getToolByName(context.getSite(), 'portal_setup')
    try:
        ps.manage_deleteImportSteps(['ckeditor-uninstall','collective.z3cform.datetimewidget','languagetool'])
        ps.manage_deleteExportSteps(['languagetool'])
    except:
        pass
    ps.runImportStepFromProfile('profile-plone.app.multilingual:default', 'plone.app.registry')
    qi = getToolByName(context.getSite(), 'portal_quickinstaller')
    qi.reinstallProducts(['PloneKeywordManager','RedirectionTool'])
    qi.installProducts(['plone.app.contenttypes'])
    qi.reinstallProducts(['plone.app.multilingual'])
