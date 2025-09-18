from .database import Base
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy import BigInteger, Column, Index, text
from sqlalchemy.orm import Mapped, mapped_column 


#This Class defines the table structure and models the data to be accepted by the health_checks table
class HealthCheck(Base):
    tablename = "health_checks"
    
    check_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True) #This is the unique id for the records in the table
    
    check_datetime = Column(
        TIMESTAMP (timezone = True),                    #Used to store the 'time instance' of when the health check is made
        nullable = False,
        server_default = text("TIMEZONE('UTC',NOW())")    #The time instance stored is in UTC    
    )
    
Index("ix_health_checks_check_datetime", HealthCheck.check_datetime)  # This creates a unique index for faster data retrivel when accessing the database 
