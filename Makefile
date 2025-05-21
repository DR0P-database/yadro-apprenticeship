db:
    docker run -d -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust --name db_random_user postgres:15
migrate:
    alembic upgrade head
configure: venv
    source ./.venv/bin/activate && pip install -r requirements.txt
venv:
    python3 -m venv .venv