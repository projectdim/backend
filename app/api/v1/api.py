from fastapi import APIRouter

from app.api.v1.endpoints import locations
from app.api.v1.endpoints import users
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import sessions

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(locations.router, prefix="/locations", tags=["locations"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(sessions.router, prefix='/sessions', tags=['sessions'])
