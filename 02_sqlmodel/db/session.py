from typing import Annotated

from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session

# create an engine
engine= create_engine(
    url="sqlite:///dummy.db",
    echo= True,
    connect_args= {
        "check_same_thread": False
    }
)

# create the tables
def create_all_tables():
    from .models import ShipmentModel
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(bind= engine) as session:
        yield session

SessionDependency= Annotated[Session, Depends(get_session)]