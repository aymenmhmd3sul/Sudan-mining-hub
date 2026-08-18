import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

def load_translation(filename):
    path = BASE_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

TRANSLATIONS = {
    "ar": load_translation("ar.json"),
    "en": load_translation("en.json"),
}
