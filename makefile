target: run_backend run_frontend

run_backend:
	pipenv run server
run_frontend:
	cd frontend && npm run dev
