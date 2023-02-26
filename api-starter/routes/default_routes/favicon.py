import os
from os.path import abspath
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

# Favicon Endpoint Route
@router.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    return FileResponse(abspath(f"{os.environ['APP_PATH']}/static/favicon.ico"))