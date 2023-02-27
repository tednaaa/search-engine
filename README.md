# Start dev server for backend & frontend

```
make -j
```

# Init Backend

```
mkdir .venv
cp .env.example .env
pipenv install
```

> .env credentials

- `SECRET_KEY`: Django secret key

# Init Frontend

```
cd frontend
cp .env.example .env
npm install
```

> .env credentials

- `PORT`: Port for local development
- `API_URL`: Api url for requesting queries to backend
