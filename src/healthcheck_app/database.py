import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv() #This loads the environment variables from the .env file

DATABASE_URL = os.getenv("DATABASE_URL") #Here we are assigning the DATABASE URL from the .env file to the variable

engine = create_engine(DATABASE_URL, echo=True) # Creating the SQlAlchemy databse engine here

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #Starting a Session

Base = declarative_base()
