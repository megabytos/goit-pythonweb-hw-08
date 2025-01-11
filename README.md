# Python Web Development HW 8 - FastAPI

## Installation

Rename .env_example to .env and edit the database credentials if necessary

```shell
mv .env_example .env
```
Run docker container with Postgres Database

```shell
sh ./postgres.sh
```
Install project dependencies

```shell
poetry install
```
Activate virtual environment

```shell
poetry shell
```
Apply database migrations

```shell
alembic upgrade head
```

## Run the Application
```shell
fastapi dev main.py
```
Test the API with Swagger: http://localhost:8000/docs