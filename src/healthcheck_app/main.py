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

def empty_response(code: int) -> Response:
    return Response(status_code=code, headers=CACHE_HEADERS)

#Creating the API endpoint which accepts GET request and checks the database connection
#Also Shows the Error when the database is down/not running
@app.get("/healthz")
async def healthz(request: Request, db: Session = Depends(get_db)) -> Response:

    # We will be returning 400 status code if the request has query parameters
    if request.query_params:
        return empty_response(status.HTTP_400_BAD_REQUEST)

    content_length = request.headers.get("content-length")
    if content_length and content_length.strip() not in ("", "0"):
        #We Return 400 if the request contains a body
        return Response(status_code=status.HTTP_400_BAD_REQUEST, headers=CACHE_HEADERS)
    
    body = await request.body()
    if body and body.strip():
        return empty_response(status.HTTP_400_BAD_REQUEST)
    
    try:
        #Creating a new Database session to perform the health check
        database = SessionLocal()
        
        #Adding the health check record into the database
        database.add(HealthCheck())
        database.commit()
        database.close()
        return Response(status_code=status.HTTP_200_OK, headers=CACHE_HEADERS)
    except (OperationalError, SQLAlchemyError):
        database.rollback()
        #We will return the Service Unavailable status when the database is not running or has errors
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, headers=CACHE_HEADERS)

#We Return an Empty Response with 405 status code when unallowed method is called
@app.post("/healthz") 
@app.put("/healthz")
@app.patch("/healthz")
@app.delete("/healthz")
def healthz_not_allowed() -> Response:
    return empty_response(status.HTTP_405_METHOD_NOT_ALLOWED)

@app.api_route("/healthz", methods=["HEAD","OPTIONS","TRACE"])
def healthz_not_allowed_meta() -> Response:
    return empty_response(status.HTTP_405_METHOD_NOT_ALLOWED)