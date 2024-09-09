import oslo_i18n

DOMAIN = 'phoenix'

_translators = oslo_i18n.TranslatorFactory(domain=DOMAIN)

_ = _translators.primary


def translate(value, user_locale):
    return oslo_i18n.translate(value, user_locale)


def get_available_languages():
    return oslo_i18n.get_available_languages(DOMAIN)
