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
def applyLanguageToContent(context):
    l = context.getSite()
    l['en'].setLanguage('en')
    l['es'].setLanguage('es')
