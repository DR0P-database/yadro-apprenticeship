run:
	source ./.venv/bin/activate && uvicorn --reload random_user_app.routes.base:app

configure: venv
	source ./.venv/bin/activate && pip install -r requirements.txt

venv:
	python3 -m venv .venv

db:
	docker run -d -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust --name db-random-user postgres:15