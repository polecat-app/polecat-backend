import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends

from app import models
from app.database import engine
from app.deps import get_current_user_from_access_token
from app.models import User
from app.routers import auth
from app.schemas import UserBaseSchema

# Setup
load_dotenv()  # Load environment variables
app = FastAPI()  # Start app
models.Base.metadata.create_all(bind=engine)  # Create ORM tables if not exist

# Include routers in app
app.include_router(auth.router)


@app.get(
    "/me",
    summary="Get details of currently logged in user",
    response_model=UserBaseSchema,
)
async def get_me(user: User = Depends(get_current_user_from_access_token)):
    return user


# RUN!!!
if __name__ == "__main__":
    uvicorn.run(app, port=int(8080), host="0.0.0.0")
