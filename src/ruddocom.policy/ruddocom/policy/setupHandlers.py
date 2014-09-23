def importLanguage(context):
    l = context.getSite()['portal_languages']
    l.manage_setLanguageSettings(
        defaultLanguage='en',
        supportedLanguages=['en', 'es'],
        setContentN=True,
        setCookieN=False,
        setCookieEverywhere=False,
        setRequestN=False,
        setPathN=False,
        setUseCombinedLanguageCodes=False,
        setCcTLDN=False,
        setSubdomainN=True,
        setForcelanguageUrls=True,
    )
