from fastapi.templating import Jinja2Templates
from app.services.i18n import translate

templates = Jinja2Templates(directory="app/templates")

def jinja_translate(key, lang="ar"):
    return translate(key, lang)

templates.env.globals["t"] = jinja_translate

templates.env.globals["t"] = translate


def template_context(request, context=None):
    if context is None:
        context = {}

    context.update({
        "lang": getattr(request.state, "lang", "ar"),
        "direction": "rtl" if getattr(request.state, "lang", "ar") == "ar" else "ltr",
    })

    return context
