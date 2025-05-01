from src.auth.models import User
from src.auth import schemas
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

class UserService:
    
    async def get_user(self, email: str, session: AsyncSession):
        """Get user by email"""
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.scalars().first()
        return user
    
    async def user_exists(self, email: str, session: AsyncSession):
        """Check if user exists by email"""
        user = await self.get_user(email, session)
        if user is not None:
            return True
        else:
            return False 
        
      



