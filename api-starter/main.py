import sys, uvicorn, time
from config.uvicorn_config import uvi_config
from config.api_logging import init_logging_local, init_logging_remote
from config.error_messages import ErrResponse
from routes import default_routes

from fastapi import FastAPI, Depends, Request

api_starter = FastAPI(
    title="API-Starter",
    docs_url=None,
    version="1.0.0",
    description="OpenAPI 3.0.2 server used for testing api routing.",
    contact={
        "name":"API-Starter",
        "url":"https://github.com/Rash-in/api-starter-project",
        "email":"jerry@bytesoffury.com"
    },
    responses={
        404: { "description": "Not Found", "model": ErrResponse },
        500: { "description": "API Server Error", "model": ErrResponse }
    }
)

@api_starter.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response

api_starter.include_router( default_routes.favicon.router )
api_starter.include_router( default_routes.healthcheck.router )
api_starter.include_router( default_routes.swagger.router)

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "local":
        server = uvicorn.Server(uvi_config)
        init_logging_local()
        try:
            server.run(); sys.exit()
        except RuntimeError as err:
            sys.exit(f"main.py local: An error occurred starting server: {err}")
    elif len(sys.argv) == 2 and sys.argv[1] == "remote":
        server = uvicorn.Server(uvi_config)
        init_logging_remote()
        try:
            server.run(); sys.exit()
        except RuntimeError as err:
            sys.exit(f"main.py remote: An error occurred starting server: {err}")
    else:
        sys.exit(f"\nArguments not satisfied.\nArgs used: {sys.argv}\nArgs required: ['main.py', 'local', 'remote']\n")
else:
    pass
# ---------------------------------------------------------------------------- #

# EOF