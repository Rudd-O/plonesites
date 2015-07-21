# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.Transform import make_config_persistent


def only_when_I_run(func):
    def importStep(context):
        if context.readDataFile('ruddocom.policy.txt') is None:
            # Not your add-on
            return
        return func(context)
    importStep.func_name = func.func_name
    return importStep


@only_when_I_run
def importLanguage(context):
    l = context.getSite()['portal_languages']
    l.force_language_urls = True


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
    l['en'].setLanguage('en')
    l['es'].setLanguage('es')

@only_when_I_run
def setCookieProperties(context):
    l = context.getSite().acl_users.session
    l.timeout = 604800
    l.cookie_lifetime = 7
    l.secure = True
