from fastapi import FastAPI, Request, Response, status
from sqlalchemy.exc import SQLAlchemyError
from .database import SessionLocal, engine, Base
from .models import HealthCheck


#Creating the API application here
app = FastAPI()

#We will be creating a table if it doesn't exist in the database
Base.metadata.create_all(bind=engine)

#Creating the API endpoint which accepts GET request and checks the database connection
#Also Shows the Error when the database is down/not running

@app.get("/healthz")
def healthz(request: Request, response: Response):
    if request.body():
        #We return 400 if the request contains a body
        response.status_code = status.HTTP_400_BAD_REQUEST  
        return
    
    #Creating a new Database session to perform the health check
    database = SessionLocal()     
    
    try:
        check = HealthCheck()
        #Adding the health check record into the database     
        database.add(check)   
        database.commit()
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.status_code = status.HTTP_200_OK
    except SQLAlchemyError:
        #We will return the Servce Unavailable status when the database is not running or has errors
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    finally:
        #Closing the database connection after completing the health check
        database.close() 
    return            