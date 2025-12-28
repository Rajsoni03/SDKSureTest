# SDKSureTest Backend (Django)

This repository hosts a Django backend for test case management with UART support, real-time updates, and REST APIs.

## Project Structure
- `test_management_backend/` – Django project root
- `config/` – settings, ASGI/WSGI, URL routing
- `apps/` – domain apps (authentication, boards, test_cases, test_execution, realtime, dashboard, configuration, core)
- `requirements/` – dependency sets for base/development/testing/production
- `docker/` – container assets
- `docs/` – setup notes

## Getting Started
1) Create a virtual environment and install deps:
```bash
python -m venv .venv
. .venv/Scripts/activate  # adjust for your shell
pip install -r test_management_backend/requirements/development.txt
```
2) Set environment variables:
```bash
cp test_management_backend/.env.example test_management_backend/.env
```
3) Run migrations and start dev server:
```bash
cd test_management_backend
python manage.py migrate
python manage.py runserver
```

## Tests
```bash
pytest
```

## Docker
```bash
docker compose up --build
```

## API Docs
- OpenAPI schema: `http://localhost:8000/api/v1/schema/`
- Swagger UI: `http://localhost:8000/api/v1/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/api/v1/schema/redoc/`


Refer to `docs/SETUP.md` for more details.
A project to test SDK before release.
