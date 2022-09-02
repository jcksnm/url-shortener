import validators

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.datastructures import URL

from . import crud, models, schemas
from .database import SessionLocal, engine
from .config import getSettings

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def getAdminInfo(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(getSettings().base_url)
    admin_endpoint = app.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url

def raiseBadRequest(message):
    raise HTTPException(status_code=400, detail=message)

def raiseNotFound(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

@app.get("/")
def readRoot():
    return "Welcome to the URL shortener API :)"

@app.post("/url", response_model=schemas.URLInfo)
def createUrl(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raiseBadRequest(message="Your provided URL is not valid")

    db_url = crud.createDbUrl(db=db, url=url)
    return getAdminInfo(db_url)


@app.get("/{url_key}")
def forwardToTargetUrl(
    url_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.getDbUrlBySecretKey(db=db, url_key=url_key):
        crud.updateDbClicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raiseNotFound(request)

@app.get(
    "/admin/{secret_key}",
    name="administration info",
    response_model=schemas.URLInfo,
)

def getUrlInfo(
    secret_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.getDbUrlBySecretKey(db, secret_key=secret_key):
        return getAdminInfo(db_url)
    else:
        raiseNotFound(request)


@app.delete("/admin/{secret_key}")
def deleteUrl(
    secret_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.deactivateDbUrlBySecretKey(
        db, secret_key=secret_key
    ):
        message = (
            f"Successfully deleted shortened URL for '{db_url.target_url}'"
        )
        return {"detail": message}
    else:
        raiseNotFound(request)