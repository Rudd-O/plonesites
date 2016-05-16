# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.Transform import make_config_persistent
from Products.CMFPlone.interfaces import ILanguage

def only_when_I_run(func):
    def importStep(context):
        if context.readDataFile('ruddocom.policy.txt') is None:
            # Not your add-on
            return
        return func(context)
    importStep.func_name = func.func_name
    return importStep


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
