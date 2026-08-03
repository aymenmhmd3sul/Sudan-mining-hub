from app.translations import TRANSLATIONS

def get_translations(lang="ar"):
    if lang not in TRANSLATIONS:
        lang = "ar"
    return TRANSLATIONS[lang]

def translate(key, lang="ar"):
    return get_translations(lang).get(key, key)
