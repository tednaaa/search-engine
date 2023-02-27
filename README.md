# Init Backend

```
mkdir .venv
cp .env.example .env
pipenv install
```

> .env credentials

- `API_SECRET`: Django secret key

# Init Frontend

```
cd frontend
cp .env.example .env
npm install
```

> .env credentials

- `PORT`: port for local development
- `API_URL`: api url for requesting queries to backend
