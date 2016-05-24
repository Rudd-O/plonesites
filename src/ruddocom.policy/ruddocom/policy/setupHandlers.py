# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.Transform import make_config_persistent
from plone.app.multilingual.browser.setup import SetupMultilingualSite
from plone.app.multilingual.interfaces import ILanguage

def only_when_I_run(func):
    def importStep(context):
        if context.readDataFile('ruddocom.policy.txt') is None:
            # Not your add-on
            return
        return func(context)
    importStep.func_name = func.func_name
    return importStep


@only_when_I_run
def setupPortalTransforms(context):
    tid = 'safe_html'

    pt = getToolByName(context, 'portal_transforms')
    if not tid in pt.objectIds(): return

    trans = pt[tid]

    permit = ["embed", "object", "style", "iframe"]

    tconfig = trans._config
    for p in permit:
        if p in tconfig['nasty_tags']: del tconfig['nasty_tags'][p]
        if p not in tconfig['valid_tags']: tconfig['valid_tags'][p] = '1'

    make_config_persistent(tconfig)
    trans._p_changed = True
    trans.reload()


@only_when_I_run
def createContent(context):
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

@only_when_I_run
def setupCookies(context):
    l = context.getSite().acl_users.session
    l.timeout = 604800
    l.cookie_lifetime = 7
    l.secure = True

@only_when_I_run
def switchToMultilingual(context):
    qi = getToolByName(context.getSite(), 'portal_quickinstaller')
    activated = False
    if not qi.isProductInstalled('plone.app.multilingual'):
        qi.installProduct('plone.app.multilingual')
        activated = True
    if not qi.isProductInstalled('archetypes.multilingual'):
        qi.installProduct('archetypes.multilingual')
        activated = True
    if qi.isProductInstalled('LinguaPlone'):
        qi.uninstallProducts(['LinguaPlone'])
    pl = getToolByName(context.getSite(), 'portal_languages')
    pl.default_language = "en"
    pl.supported_langs = ['en', 'es']
    pl.use_cookie_negotiation = False
    pl.use_subdomain_negotiation = True
    if activated:
        s = SetupMultilingualSite(context=context.getSite())
        s.setupSite(context.getSite())

@only_when_I_run
def cleanupBeforeUpgrade(context):
    qi = getToolByName(context.getSite(), 'portal_quickinstaller')
    qi.uninstallProducts(['collective.ckeditor', 'collective.plonefinder', 'collective.quickupload', 'collective.searchandreplace'])
    catalog = getToolByName(context.getSite(), 'portal_catalog')
    catalog.refreshCatalog(clear=1)
