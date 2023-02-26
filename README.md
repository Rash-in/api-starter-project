# api-starter (NOT YET FUNCTIONING OR TO BE USED FOR PRODUCTION LEVEL DEPLOY)


pip install pipdeptree colander fastapi gunicorn uvicorn loguru mysqlclient pytest setproctitle python-dotenv sqlalchemy
requests poetry wheel setuptools

python -m pip install --upgrade wheel setuptools

pip freeze > src/requirements.txt

be in api-starter
poetry init
- add the deps manually
ipdeptree colander fastapi gunicorn uvicorn loguru mysqlclient pytest setproctitle python-dotenv sqlalchemy
requests poetry wheel setuptools

poetry install

setup runtime folder
in terminal cd to where all repos are stored.
`mkdir Runtime`
`mkdir -p /path/to/Runtime/bin /path/to/Runtime/certs /path/to/Runtime/envs /path/to/Runtime/logs /path/to/Runtime/pids`
`cd /path/to/Runtime/envs`
`touch api-starter.env`

`ln -s /path/to/api-starter-project /path/to/Runtime`

