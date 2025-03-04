from fastapi import Depends
from sqlmodel import Session
from ..db.database import db_manager
from typing import Generator

def get_db() -> Generator[Session, None, None]:
    try:
        db = next(db_manager.get_session())
        yield db
    finally:
        db.close()

SessionDep = Depends(get_db)