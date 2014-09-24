def importLanguage(context):

    if context.readDataFile('ruddocom.policy.txt') is None:
        # Not your add-on
        return

    l = context.getSite()['portal_languages']
    l.force_language_urls = True
