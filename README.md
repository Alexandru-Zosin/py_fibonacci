# Py‑Fibonacci Micro‑service

A lightweight Flask API that computes Fibonacci, power, and factorial operations, while logging each request to an Oracle XE database. Everything runs in Docker—get started with one command.

**Chirila Sabin** - development of 3 API endpoints for mathematical operations: power, factorial, and Fibonacci. I used Pydantic for input data validation, ensuring they are positive integers. I implemented asynchronous operation execution, using **asyncio** and a queue (asyncio.Queue) with a background worker for parallel processing. Each request is logged in the Oracle database.

**Rares-Stefan Cazan** - delivered the end-to-end delivery of this microservice suite by crafting all responsive front-end interfaces (login, registration, and dashboard); building secure login and registration REST endpoints; architecting an Oracle-backed persistence layer via SQLAlchemy; structuring everything in a clean MVC pattern with views, controllers, and models; exposing APIs while capturing each user’s request history, and integrating async workers, authentication flows, and database operations into a production-ready, cohesive microservice solution.

## 1. Project Overview
- **Model**: Pure‑Python logic (`FibonacciOperation`, `PowerOperation`, `FactorialOperation`) and SQLAlchemy entities (`User`, `APILog`).
- **View**: Jinja2 templates for login, registration, dashboard, and history.
- **Controller**: Flask routes (`/pow`, `/fibonacci`, `/factorial`, `/auth/*`) with async task‑offloading via an in‑process worker queue.
- **Database**: Oracle 21c XE, initialized by `db/init.sql` on container start.
- **Worker**: `workers.py` processes queued tasks, keeping web threads responsive.

## 2. Prerequisites
- **Docker** ≥ 20.10
- **Docker Compose** v2 or `docker-compose`
- **Oracle Container Registry** account (to pull `oracle.com/database/express:latest`)

> **Note**: Oracle XE runs in its container—no local install needed.

## 3. Quick Start
```bash
git clone https://github.com/Alexandru-Zosin/py_fibonacci.git
cd py_fibonacci
cp .env.example .env  # edit with your credentials
docker compose up --build
# Visit http://localhost:8000/health to confirm status
```
- **Services**:
  - **oracle-db**: runs Oracle XE, executes `init.sql` to create users and tables.
  - **fibonacci-service**: waits for DB health, then launches Flask/Gunicorn on port 8000.
- **Flow**: Requests to `/fibonacci`, `/pow`, or `/factorial` are logged, queued, computed asynchronously, then returned as JSON.

## 4. Building the Docker Image
```bash
docker build -t fibonacci-service:latest .
```
- Reuse the image by adding `image: fibonacci-service:latest` in `docker-compose.yml` to skip rebuilds.

## 5. Development Mode
In `docker-compose.yml`:
```yaml
fibonacci-service:
  build: .
  volumes:
    - ./app:/usr/src/app/app
  command: flask --app app.Controller.app --debug run --host 0.0.0.0
```
Code changes auto‑reload; remove `volumes:` for production build.

## 6. Environment Variables
| Variable         | Purpose                                              |
|------------------|------------------------------------------------------|
| ORACLE_PWD       | SYS/SYSTEM password on first boot                    |
| ORACLE_USER      | Application DB user (from `init.sql`)                |
| ORACLE_PASSWORD  | Password for `ORACLE_USER`                           |
| ORACLE_HOST      | DB host (Docker service name)                        |
| ORACLE_PORT      | DB listener port (default 1521)                      |
| ORACLE_SERVICE   | PDB service name (e.g., `xepdb1`)                    |

Place them in `.env` so both services inherit them.

## 7. API Endpoints
| Endpoint       | Method | Body                        | Response      |
|----------------|--------|-----------------------------|---------------|
| `/pow`         | POST   | `{ "base": 2, "exponent": 10 }` | `1024`        |
| `/fibonacci`   | POST   | `{ "n": 15 }`             | `610`         |
| `/factorial`   | POST   | `{ "n": 7 }`              | `5040`        |
| `/auth/*`      | GET/POST | Form data                 | User/session  |
| `/health`      | GET    | —                           | `{ "status":"up","db":1 }` |

## 8. Project Structure
```
├── app
│   ├── Controller
│   │   ├── app.py
│   │   └── auth_controller.py
│   ├── Model
│   │   ├── problem_model.py
│   │   ├── user_model.py
│   │   └── log_model.py
│   ├── View
│   │   ├── Html/…
│   │   └── static/…
│   └── workers.py
├── db/init.sql
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## 9. Troubleshooting
- **`unauthorized: authentication required`**: Run `docker login container-registry.oracle.com`.
- **`ORA-12541: TNS:no listener`**: DB not ready—run `docker compose ps` and wait for `healthy`.
- **Health check `db-error`**: Verify `init.sql` ran and credentials in `.env` match.

