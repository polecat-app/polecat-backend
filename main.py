import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends

from app import models
from app.config import settings
from app.database import engine
from app.deps import get_current_user_from_access_token
from app.models import User
from app.routers import auth, save
from app.schemas import UserBaseSchema

# Setup
load_dotenv()  # Load environment variables
app = FastAPI()  # Start app
models.Base.metadata.create_all(bind=engine)  # Create ORM tables if not exist

# Include routers in app
app.include_router(auth.router)
app.include_router(save.router)


# RUN!!!
if __name__ == "__main__":
    if settings.HOST:
        uvicorn.run("main:app", port=8080, host=settings.HOST, reload=True)
    else:
        uvicorn.run(app, port=8080, host="0.0.0.0")
