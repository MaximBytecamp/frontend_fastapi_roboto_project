from contextlib import asynccontextmanager 

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles 

from app.core.config import settings
from app.core.database import create_db_and_tables 

from app.routers import auth, profile

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    from app.seed import seed_data
    seed_data()

    yield 


app = FastAPI(title=settings.PROJECT_NAME, description=settings.PROJECT_DESCRIPTION, lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(profile.router)