init_project:
	mkdir .venv
	cp .env.example .env
	pipenv shell
	pipenv install --ignore-pipfile

	cd frontend
	cp .env.example .env
	npm ci
