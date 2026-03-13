# Decision Log

## Layered Architecture (Domain / Application / Infrastructure)

The project is organized in three layers:

- **domain** — core models and exceptions, no external dependencies
- **application** — business logic (services), uses the domain layer
- **infrastructure** — database, repositories, FastAPI routes, config

This separation keeps the business logic independent from the framework and the database. It also makes testing easier because each layer can be tested in isolation.

## Python 3.12-slim

`python:3.12-slim` is used as the base Docker image. The `slim` variant removes tools that are not needed to run the application (like compilers and documentation). This results in a smaller and faster image.

## FastAPI 0.135

Chosen because it is fast, modern, and easy to use. It generates automatic documentation (Swagger) and has built-in support for data validation with Pydantic.

## PostgreSQL 16

Chosen as the main database because it is reliable and works well with SQLAlchemy. It runs in Docker so no local installation is needed.

## SQLAlchemy 2.0

Chosen as the ORM to interact with the database. It supports multiple databases, which makes it easy to use SQLite in tests and PostgreSQL in production without changing any code.

## Pydantic 2.12 + pydantic-settings 2.13

Used for request and response validation. It is already included with FastAPI and makes it simple to define data schemas with type hints. `pydantic-settings` is used to load configuration from the `.env` file.

## JWT (python-jose 3.5)

Chosen for authentication because it is stateless. The server does not need to store sessions. The token contains the user ID and expires after a set time.

## Docker + Docker Compose

Chosen to make the project easy to run on any machine. Everything runs in containers, so there is no need to install Python, PostgreSQL, or any dependency manually.

## pytest 9.0

Chosen for testing. It is the standard testing tool in Python. The tests use FastAPI's `TestClient` to make HTTP requests without starting a real server. `httpx 0.28` is listed in requirements because `TestClient` needs it internally, but it is not used directly in the code.

## flake8 7.3 + black 26.3 + isort 8.0

Chosen to keep the code clean and consistent. `black` formats the code automatically, `isort` organizes the imports, and `flake8` checks for errors and style issues. `flake8` is configured with `max-line-length = 88` to match `black`.

## passlib 1.7 + bcrypt 3.2

Used to hash and verify passwords. `passlib` provides a simple API for password hashing. `bcrypt` is the hashing algorithm, which is slow by design — this makes it hard for attackers to crack passwords with brute force. `bcrypt` is pinned to version `3.2.2` because newer versions break compatibility with `passlib 1.7`.
