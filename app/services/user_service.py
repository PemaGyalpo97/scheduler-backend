import datetime
from app.models.user_model import UserRegistration, PersonalDetail, UserDetail
from app.schemas.user_schema import UserRegistrationCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.utils.security import hash_password, verify_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, user_data: UserRegistrationCreate):
        user = UserRegistration(**user_data.dict())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def approve_user(self, id: int, role: str):
        # Fetch the user from the registration table
        user = await self.db.get(UserRegistration, id)
        if not user:
            return None  # Or raise an exception

        # Create a new PersonalDetail record
        personal_detail = PersonalDetail(
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name,
            email=user.email,
            role=role,
            is_active=True,
            created_at=user.created_at,
            created_by=user.created_by,
            updated_at=user.created_at,
            updated_by=user.created_by
        )
        
        # Create a new UserDetail record
        user_detail = UserDetail(
            login_id=user.email,
            password=hash_password(user.first_name+str(datetime.date.today().year)),
            created_at=user.created_at,
            created_by=user.created_by,
            updated_at=user.created_at,
            updated_by=user.created_by
        )
        print("password", user.first_name+str(datetime.date.today().year))
        
        # Add to user_detail
        self.db.add(user_detail)
        await self.db.commit()
        await self.db.refresh(user_detail)
        
        # Add to personal_detail and delete from registration
        self.db.add(personal_detail)
        await self.db.delete(user)
        await self.db.commit()
        await self.db.refresh(personal_detail)

        return personal_detail

    async def login_user(self, login_id: str, password: str):
        result = await self.db.execute(select(UserDetail).where(UserDetail.login_id == login_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        return {"message": "Login successful"}