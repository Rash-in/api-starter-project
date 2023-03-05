import sys, uvicorn, time, argparse
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



# ----------------------------- RUNTIME EXECUTION ---------------------------- #
parser = argparse.ArgumentParser(
    prog='api-starter.py',
    description='OpenAPI 3.0.2 server used for testing api routing.',
    epilog='''---'''
)
parser.add_argument('-e', '--environment', type=str, required=True, choices=['local', 'remote'] , help='Path to dotenv file to load. If none present runs app without like a remote deploy.')
args = parser.parse_args()
environment = args.environment

def main(environment=environment):
    server = uvicorn.Server(uvi_config)
    if environment == 'local':
        init_logging_local()
    elif environment == 'remote':
        init_logging_remote()
    else:
        raise ValueError("No environment selected. Something is wrong.")
    
    try:
        server.run(); sys.exit()
    except RuntimeError as err:
        sys.exit(f"main.py local: An error occurred starting server: {err}")

if __name__ == "__main__":
    main()
# ---------------------------------------------------------------------------- #

# EOF