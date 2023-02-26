from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html

router = APIRouter()

# Swagger UI Endpoint Route
@router.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url = "/openapi.json",
        swagger_favicon_url = "/favicon.ico",
        title="TCC Tools API",
        swagger_ui_parameters={
            "syntaxHighlight.theme":"obsidian",
            "docExpansion":"None",
            "defaultModelsExpandDepth":0
        }
    )