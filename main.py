# Code from : https://github.com/tiangolo/fastapi/issues/364

## Main
from fastapi import FastAPI
import uvicorn, os
## Security Basic Auth
import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
## Add Doc Security
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

## Initial App
app = FastAPI(
    title="FastAPI",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

## Initial Basic Auth
security = HTTPBasic()


## For document
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "user")
    correct_password = secrets.compare_digest(credentials.password, "password")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={
                "WWW-Authenticate": "Basic"},
        )
    return credentials.username


## For actual API => to aviod Authentication header from GCP's bearer token
def weak_authentication(credentials: dict):
    weak_key = credentials.get('weak_authen', '')
    if weak_key != "temporary_work":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={
                "WWW-Authenticate": "Basic"},
        )
    return 'authen_ok'


## Create Auth Doc
@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(username: str = Depends(get_current_username)):
    return get_redoc_html(openapi_url="/openapi.json", title="docs")


## API Function, use POST because GCP's authentication does not allow body in GET
@app.post("/myapi")
async def myapi(username: str = Depends(weak_authentication)):
    return {
        'status': username,
        'hello': 'world'}


## RUN!!!
if __name__ == "__main__":
    uvicorn.run(app, port=int(os.environ.get("PORT", 8000)), host="0.0.0.0")