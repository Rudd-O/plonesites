# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.Transform import make_config_persistent
from Products.CMFPlone.interfaces import ILanguage

default_profile = 'profile-ruddocom.policy:default'

def only_when_I_run(func):
    def importStep(context):
        if context.readDataFile('ruddocom.policy.txt') is None:
            # Not your add-on
            return
        return func(context)
    importStep.func_name = func.func_name
    return importStep


def createContent(context):
    import sys
    l = context.getSite().portal_quickinstaller.isProductInstalled('Products.ATContentTypes')
    print >> sys.stderr, "\nFUCK", l, "\n"
    logger = context.getLogger('ruddocom.policy')
    logger.info("Creating content")
    l = context.getSite()
    if "en" not in l:
        l.invokeFactory("ATFolder", "en")
    if "es" not in l:
        l.invokeFactory("ATFolder", "es")
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
    datafile = context.readDataFile('ruddocom.policy.txt') if hasattr(context, 'readDataFile') else None
    if datafile is None:
        # Not your add-on
        return
    logger = context.getLogger('ruddocom.policy')
    logger.info("Beginning setupAll with context %s", context)
    setupCookies(context)
    createContent(context)

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
