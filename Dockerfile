FROM python:3.10-alpine

ARG YOUR_ENV

RUN apk add --no-cache build-base gcc make tzdata

ENV YOUR_ENV=${YOUR_ENV} \
    TZ=America/Chicago \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.12

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false \
    && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

COPY . /code

CMD ["python3", "-B" , "bin/api-starter.py", "remote"]