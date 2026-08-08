from fastapi.templating import Jinja2Templates
from jinja2 import pass_context

from app.services.i18n import translate


class CentralTemplates(Jinja2Templates):
    """
    Central template engine for the whole platform.
    Automatically injects language and direction.
    """

    def TemplateResponse(self, *args, **kwargs):
        request = kwargs.get("request")

        if request is None and args:
            if hasattr(args[0], "state"):
                request = args[0]

        context = kwargs.get("context")

        if context is None:
            context = {}
        else:
            context = dict(context)

        if request is not None:
            lang = getattr(request.state, "lang", "ar")

            context.setdefault("lang", lang)
            context.setdefault(
                "direction",
                "rtl" if lang == "ar" else "ltr"
            )

        kwargs["context"] = context

        return super().TemplateResponse(*args, **kwargs)


templates = CentralTemplates(directory="app/templates")


@pass_context
def jinja_translate(context, key, default=None):
    lang = context.get("lang", "ar")

    result = translate(key, lang)

    if result == key and default is not None:
        return default

    return result


templates.env.globals["t"] = jinja_translate


def template_context(request, context=None):
    if context is None:
        context = {}

    context = dict(context)

    lang = getattr(request.state, "lang", "ar")

    context.update({
        "lang": lang,
        "direction": "rtl" if lang == "ar" else "ltr",
    })

    return context
