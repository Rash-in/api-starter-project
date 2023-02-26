import os
from os.path import abspath
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

# Healthcheck Endpoint Route
@router.get("/healthcheck/index.html", include_in_schema=False)
async def get_healthcheck():
    return FileResponse(abspath(f"{os.environ['APP_PATH']}/static/healthcheck/index.html"))