from fastapi import APIRouter

from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.language import router as language_router
from app.api.v1.routes.problems import router as problems_router
from app.api.v1.routes.submission import router as submission_router
from app.api.v1.routes.leaderboard import router as leaderboard_router
from app.api.v1.routes.ws import (
    router as ws_router,
)
from app.api.v1.routes.users import router as users_router
from app.api.v1.routes.test_case import router as test_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(language_router)
api_router.include_router(problems_router)
api_router.include_router(submission_router)
api_router.include_router(leaderboard_router)
api_router.include_router(ws_router)
api_router.include_router(test_router)