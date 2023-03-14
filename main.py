import os
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI, Depends

from app import models
from app.database import engine
from app.deps import get_current_user
from app.models import User
from app.routers import auth
from app.schemas import UserBaseSchema

load_dotenv()
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Include auth router in app
app.include_router(auth.router)


@app.get('/me', summary='Get details of currently logged in user', response_model=UserBaseSchema)
async def get_me(user: User = Depends(get_current_user)):
    return user


## RUN!!!
if __name__ == "__main__":
    uvicorn.run(app, port=int(os.getenv("PORT", 8000)), host="0.0.0.0")