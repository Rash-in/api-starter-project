import os, sys, logging
from loguru import logger

repo_path = os.path.dirname(os.environ['APP_PATH'])

# -------------- Pipe Loguru logger into standard python logging ------------- #
class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
# ---------------------------------------------------------------------------- #

# ------------------------- Define Loguru Formatting ------------------------- #
fmt = (
    "<green>[{time:YYYY-MM-DDTHH:mm:ssZ}]</green> | "
    "<yellow>{extra[platform]}: {extra[instance]}</yellow> | "
    "<cyan>{level}      </cyan>"
    "<bold>{message}</bold>"
)
# ---------------------------------------------------------------------------- #
def init_logging():
    logging.getLogger("uvicorn.access").propagate = False
    logging.getLogger("uvicorn.error").propagate = False
    logging.getLogger("uvicorn.error").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]

    logger.configure(
        extra={
            "platform":os.environ['PLATFORM'],
            "instance":os.environ['INSTANCE']
        },
        handlers=[
            {   # Remote logger (logs to file)
                "sink": f"{os.environ['LOG_PATH']}/{os.environ['INSTANCE']}.log", 
                "level": "TRACE",
                "format":fmt,
                "backtrace":False,
                "colorize": False,
                "diagnose":False,
                "rotation":"10 days"
            },
            {   # Local logger (stdout)
                "sink": sys.stdout,
                "level": "TRACE",
                "format": fmt,
                "colorize":True,
                "backtrace": True,
                "diagnose":True
            }
        ]
    )
    logger.level(name="API_CATCH", no=50)
    logger.level(name="API_CODING", no=50)
    logger.level(name="API_INCOMPLETE", no=40)
    logger.level(name="API_BAD_DATA", no=30)
    logger.level(name="API_NOTFOUND", no=30)
    logger.level(name="API_COMPLETE", no=25)
    logger.level(name="API_DEBUG", no=5)
# ---------------------------------------------------------------------------- #

# EOF