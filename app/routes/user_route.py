from fastapi import APIRouter, Depends
from app.database.session import get_db
from app.schemas.user_schema import UserRegistrationCreate, LoginRequest, LoginResponse
from app.services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
async def register_user(user: UserRegistrationCreate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.register_user(user)

@router.post("/approve_user/{id}/{role}")
async def approve_user(id: int, role: str, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.approve_user(id,role)

@router.post("/users/login", response_model=LoginResponse)
async def login_user(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.login_user(payload.login_id, payload.password)