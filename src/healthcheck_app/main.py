from fastapi import FastAPI, Request, Depends, status
from fastapi.responses import Response
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import HealthCheck


#Creating the API application here
app = FastAPI()

#We will be creating a table if it doesn't exist in the database
Base.metadata.create_all(bind=engine)

def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

CACHE_HEADERS = {
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "X-Content-Type-Options": "nosniff",
}

#Creating the API endpoint which accepts GET request and checks the database connection
#Also Shows the Error when the database is down/not running
@app.get("/healthz")
def healthz(request: Request):

    content_length = request.headers.get("content-length")
    if content_length and content_length.strip() not in ("", "0"):
        #We Return 400 if the request contains a body
        return Response(status_code=status.HTTP_400_BAD_REQUEST, headers=CACHE_HEADERS)

    try:
        #Creating a new Database session to perform the health check
        database = SessionLocal()
        
        #Adding the health check record into the database
        database.add(HealthCheck())
        database.commit()
        database.close()
        return Response(status_code=status.HTTP_200_OK, headers=CACHE_HEADERS)
    except (OperationalError, SQLAlchemyError):
        #We will return the Service Unavailable status when the database is not running or has errors
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, headers=CACHE_HEADERS)