from flask import session
from src.auth.models import User
from src.auth import schemas, utils
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

class UserService:
    
    async def get_user(self, email: str, session: AsyncSession):
        """Get user by email"""
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalars().first()
        return user
    
    async def user_exists(self, email: str, session: AsyncSession):
        """Check if user exists by email"""
        user = await self.get_user(email, session)
        if user is not None:
            return True
        else:
            return False 
        
    async def create_user(self, user_data: schemas.UserCreateModel, session: AsyncSession):  
        
        user_data_dict = user_data.model_dump()
        
        new_user = User(
            **user_data_dict
        )

        new_user.password_hash = utils.generate_password_hash(user_data_dict["password"])
              
        session.add(new_user)
        await session.commit()
        
        return new_user
