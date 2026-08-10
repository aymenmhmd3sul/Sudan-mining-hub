from typing import Optional
from app.translations import TRANSLATIONS


SUPPORTED_LANGUAGES = ("ar", "en")
DEFAULT_LANGUAGE = "ar"


def normalize_language(lang: Optional[str]) -> str:
    """
    توحيد اللغة والتحقق منها.
    """
    if lang in SUPPORTED_LANGUAGES:
        return lang
    return DEFAULT_LANGUAGE


def get_translations(lang: Optional[str] = None):
    """
    إرجاع قاموس الترجمة للغة المطلوبة.
    """
    lang = normalize_language(lang)
    return TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANGUAGE])


def translate(key: str, lang: Optional[str] = None) -> str:
    """
    ترجمة مفتاح واحد.

    إذا لم توجد الترجمة، يعاد المفتاح نفسه بدلاً من كسر الصفحة.
    """
    translations = get_translations(lang)
    return translations.get(key, key)


def language_direction(lang: Optional[str] = None) -> str:
    """
    اتجاه الواجهة حسب اللغة.
    """
    return "rtl" if normalize_language(lang) == "ar" else "ltr"
