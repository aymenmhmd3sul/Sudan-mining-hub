import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TRANSLATION_DIR = BASE_DIR / "translations"


def load_language(lang="ar"):
    file = TRANSLATION_DIR / f"{lang}.json"

    if not file.exists():
        file = TRANSLATION_DIR / "ar.json"

    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def translate(key, lang="ar"):
    data = load_language(lang)
    return data.get(key, key)
