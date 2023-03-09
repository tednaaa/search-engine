target: run_backend run_frontend

run_backend:
	cd backend && pipenv run server
run_frontend:
	cd ../frontend && npm run dev

load_dataset:
	cd backend && python load_dataset.py bitcoin
