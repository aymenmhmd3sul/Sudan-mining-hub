from pathlib import Path

from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.services.i18n import translate


TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


class UnifiedTemplates(Jinja2Templates):
    """
    طبقة موحدة لعرض القوالب.

    تدعم الاستدعاءات الحالية سواء:
        TemplateResponse("page.html", context)
    أو:
        TemplateResponse(request=request, name="page.html", context=context)

    وتضمن تمرير request + اللغة + الاتجاه إلى جميع القوالب.
    """

    def __init__(self, directory):
        super().__init__(directory=directory)

        # دالة الترجمة متاحة مباشرة داخل Jinja:
        # {{ t("login") }}
        self.env.globals["t"] = translate

    def TemplateResponse(self, *args, **kwargs):
        """
        Compatibility wrapper حول Jinja2Templates.TemplateResponse.
        """

        request = kwargs.pop("request", None)
        name = kwargs.pop("name", None)
        context = kwargs.pop("context", None)

        # --------------------------------------------------
        # دعم الاستدعاء القديم:
        # TemplateResponse("page.html", {"request": request})
        # --------------------------------------------------
        if args:
            if isinstance(args[0], str):
                if name is None:
                    name = args[0]

                if len(args) > 1 and context is None:
                    context = args[1]

                if len(args) > 2 and request is None:
                    request = args[2]

            elif isinstance(args[0], Request):
                if request is None:
                    request = args[0]

                if len(args) > 1 and name is None:
                    name = args[1]

                if len(args) > 2 and context is None:
                    context = args[2]

        # --------------------------------------------------
        # حماية من أي استدعاء ناقص
        # --------------------------------------------------
        if not name:
            raise ValueError("TemplateResponse requires a template name")

        if context is None:
            context = {}

        if not isinstance(context, dict):
            context = dict(context)

        # request يمكن أن يكون داخل context في بعض القوالب القديمة
        if request is None:
            request = context.get("request")

        if request is not None:
            context.setdefault("request", request)

            # اللغة والاتجاه
            lang = getattr(
                getattr(request, "state", None),
                "lang",
                None
            )

            direction = getattr(
                getattr(request, "state", None),
                "direction",
                None
            )

            if not lang:
                lang = "ar"

            if not direction:
                direction = "rtl" if lang == "ar" else "ltr"

            context.setdefault("lang", lang)
            context.setdefault("direction", direction)

        else:
            context.setdefault("lang", "ar")
            context.setdefault("direction", "rtl")

        return super().TemplateResponse(
            request=request,
            name=name,
            context=context,
            **kwargs
        )


templates = UnifiedTemplates(str(TEMPLATES_DIR))


def template_context(request: Request, context=None):
    """
    السياق الموحد لجميع صفحات المنصة.
    """

    data = dict(context or {})

    lang = getattr(
        getattr(request, "state", None),
        "lang",
        None
    ) or "ar"

    direction = getattr(
        getattr(request, "state", None),
        "direction",
        None
    )

    if not direction:
        direction = "rtl" if lang == "ar" else "ltr"

    data["request"] = request
    data["lang"] = lang
    data["direction"] = direction

    return data
