from pathlib import Path

from fastapi import Request
from fastapi.templating import Jinja2Templates
from jinja2 import pass_context

from app.services.i18n import (
    DEFAULT_LANGUAGE,
    language_direction,
    normalize_language,
    translate,
)


TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


class UnifiedTemplates(Jinja2Templates):
    """
    طبقة موحدة لعرض القوالب.

    تدعم الاستدعاءات القديمة والجديدة لـ TemplateResponse،
    وتضمن تمرير request واللغة والاتجاه إلى القالب.

    كما تجعل:
        {{ t("login") }}

    تعتمد تلقائياً على لغة الطلب الحالية بدلاً من افتراض العربية.
    """

    def __init__(self, directory):
        super().__init__(directory=directory)

        @pass_context
        def jinja_translate(context, key, lang=None):
            """
            ترجمة واعية بسياق Jinja.

            الأولوية:
            1. lang المرسل صراحة
            2. lang الموجود في context
            3. request.state.lang
            4. العربية كافتراضي
            """
            if lang is None:
                lang = context.get("lang")

            if lang is None:
                request = context.get("request")
                if request is not None:
                    lang = getattr(
                        getattr(request, "state", None),
                        "lang",
                        None,
                    )

            lang = normalize_language(lang or DEFAULT_LANGUAGE)
            return translate(key, lang)

        self.env.globals["t"] = jinja_translate
        self.env.globals["language_direction"] = language_direction
        self.env.globals["normalize_language"] = normalize_language

    def TemplateResponse(self, *args, **kwargs):
        """
        Compatibility wrapper حول Jinja2Templates.TemplateResponse.
        يدعم الصيغ القديمة والجديدة.
        """

        request = kwargs.pop("request", None)
        name = kwargs.pop("name", None)
        context = kwargs.pop("context", None)

        # الصيغة القديمة:
        # TemplateResponse("page.html", {"request": request})
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

        if not name:
            raise ValueError(
                "TemplateResponse requires a template name"
            )

        if context is None:
            context = {}

        if not isinstance(context, dict):
            context = dict(context)

        # بعض القوالب القديمة تمرر request داخل context
        if request is None:
            request = context.get("request")

        if request is not None:
            context.setdefault("request", request)

            state = getattr(request, "state", None)

            lang = getattr(
                state,
                "lang",
                None,
            )

            direction = getattr(
                state,
                "direction",
                None,
            )

            lang = normalize_language(lang)

            if not direction:
                direction = language_direction(lang)

            context.setdefault("lang", lang)
            context.setdefault("direction", direction)

        else:
            context.setdefault("lang", DEFAULT_LANGUAGE)
            context.setdefault("direction", "rtl")

        return super().TemplateResponse(
            request=request,
            name=name,
            context=context,
            **kwargs,
        )


templates = UnifiedTemplates(str(TEMPLATES_DIR))


def template_context(request: Request, context=None):
    """
    السياق الموحد لجميع صفحات المنصة.
    """

    data = dict(context or {})

    state = getattr(request, "state", None)

    lang = normalize_language(
        getattr(state, "lang", None)
    )

    direction = getattr(
        state,
        "direction",
        None,
    ) or language_direction(lang)

    data["request"] = request
    data["lang"] = lang
    data["direction"] = direction

    return data
