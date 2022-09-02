from sqlalchemy.orm import Session
from . import keygen, models, schemas

def createDbUrl(db: Session, url: schemas.URLBase) -> models.URL:
    key = keygen.createUniqueRandomKey(db)
    secret_key = f"{key}_{keygen.createRandomKey(length=8)}"
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def getDbUrlByKey(db: Session, url_key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )

def getDbUrlBySecretKey(db: Session, secret_key: str) -> models.URL:
    return(
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )

def updateDbClicks(db: Session, db_url: schemas.URL) -> models.URL:
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url

def deactivateDbUrlBySecretKey(
    db: Session, secret_key: str
) -> models.URL:
    db_url = getDbUrlBySecretKey(db, secret_key)
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url