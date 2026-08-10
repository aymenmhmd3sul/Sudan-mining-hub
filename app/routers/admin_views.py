import os

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from app.services.templates import templates, template_context
from app.core.dependencies import verify_admin_token


router = APIRouter(
    prefix="/admin",
    tags=["Admin Views"]
)


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, current_user=Depends(verify_admin_token)):
    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context=template_context(
            request,
            {
                "active_tab": "dashboard"
            }
        )
    )


# ============================================================
# ADMIN MODULE ROUTER
# ============================================================

@router.get("/{module_name}", response_class=HTMLResponse)
@router.get("/{module_name}/{subpath:path}", response_class=HTMLResponse)
async def render_admin_module(
    request: Request,
    module_name: str,
    subpath: str = "",
    current_user=Depends(verify_admin_token),
):

    # --------------------------------------------------------
    # Escrow special route
    # --------------------------------------------------------

    if module_name == "finance" and subpath == "escrow":

        return templates.TemplateResponse(
            request=request,
            name="admin/finance/escrow.html",
            context=template_context(
                request,
                {
                    "active_tab": "escrow"
                }
            )
        )

    # --------------------------------------------------------
    # Normalize module name
    # --------------------------------------------------------

    normalized_module = module_name.replace("-", "_")

    # --------------------------------------------------------
    # First try sub-module template
    #
    # Example:
    # /admin/marketplace/buys
    #
    # -> admin/marketplace/buys/index.html
    # --------------------------------------------------------

    if subpath:

        normalized_subpath = subpath.strip("/")

        sub_template_path = (
            f"admin/{normalized_module}/"
            f"{normalized_subpath}/index.html"
        )

        sub_full_path = os.path.join(
            "app/templates",
            sub_template_path
        )

        if os.path.exists(sub_full_path):

            context = template_context(
                request,
                {
                    "active_tab": module_name,
                    "room_id": normalized_subpath
                }
            )

            return templates.TemplateResponse(
                request=request,
                name=sub_template_path,
                context=context
            )

    # --------------------------------------------------------
    # Standard module template
    #
    # Example:
    # /admin/marketplace
    #
    # -> admin/marketplace/index.html
    # --------------------------------------------------------

    template_path = (
        f"admin/{normalized_module}/index.html"
    )

    full_path = os.path.join(
        "app/templates",
        template_path
    )

    context = template_context(
        request,
        {
            "active_tab": module_name,
            "room_id": subpath if subpath else "1"
        }
    )

    if os.path.exists(full_path):

        return templates.TemplateResponse(
            request=request,
            name=template_path,
            context=context
        )

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context=context
    )
