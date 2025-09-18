#Health Check API

This is a Cloud-native health checking serivice  built in python using FastAPI , PostgreSQL, SQLAlchemy and Alembic
It demonstares the Automatic schema management, Zero manual intervention and  ORM-Driven Migration

## Tech Stack used

- [Uvicorn]- ASGI server
- [FastAPI] - API framework
- [PostgreSQL] - Database
- [SQLAlchemy] - ORM
- [Alembic] - Migrations

# Project Structure

Cloud-WebApp/
|------ src/
|      --- healthcheck_app/
|          ---- init.py
|          ---- .env
|          ---- database.py
|          ---- models.py
|          ---- main.py
|          ---- alembic 
|          ---- requirements.txt
|      ---- .gitignore 
|      ---- README.md 

## Features

- /healthz endpoint
  - It Returns '200 OK' if the service and the Database are healthy
  - It wil Return '503 Service unavailable' if the Database is down or has errors
  - Returns '400 Bad Request' if request includes body or has query parameters
  - It Returns '405 Method Not Allowed' for unsupported HTTP Methods
  - All the responses from the requests are empty body with correct headers


- Database Automation
  - The tables and schema are auto-created using SQLAlchemy models
  - Alembic is used for the schema migrations


## Setup 

- Clone the repo and change the working directory to the root directory

- Now create the virtual environment using ' python3 -m venv .venv source .vinv/bin/activate

- Install the dependencies using " pip3 install -r requirements.txt "

- Create the database for health checks(healthz-db) using the commands "CREATE DATABSE healthz_db;
- CREATE USER <username> WITH PASSWORD <password>;
- GRANT ALL PRIVILAGES ON DATABASE healthz_db TO <username>
- copy the DATABASEURL into the .env file
 

- Run the Alembic migration by "alembic upgrade head"

- Start the app using the command 'univorn main:app --reload --port 8080'



## API USAGE 

- Commands to test the API
  
  - Basic health check request (GET Request)
    - 'curl -i http://127.0.0.1:8080/healthz 

  - health check request with Body
    - 'curl -i -X GET http://127.0.0.1:8080/healthz -d '{"test":"data"} -H "Content-Type: application/json" 

  - Making a GET request when the Database is down ( First stop the PostgreSQL service)
    - 'curl -i http://127.0.0.1:8080/healthz

  - Testing the unsupported methods
    - 'curl -i -X POST http://127.0.0.1:8080/healthz  




