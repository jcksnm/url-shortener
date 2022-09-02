import secrets
import string
from sqlalchemy.orm import Session
from . import crud

def createRandomKey(length: int = 5) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

def createUniqueRandomKey(db: Session) -> str:
    key = createRandomKey()
    while crud.getDbUrlByKey(db, key):
        key = createRandomKey()
    return key