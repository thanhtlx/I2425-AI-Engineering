from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from main.models import StateModel


async def get_state(session: AsyncSession, state_id: int) -> StateModel | None:
    stmt = select(StateModel).where(StateModel.id == state_id)
    stmt = stmt.where(StateModel.is_deleted.is_(False))
    result = await session.execute(stmt)
    return result.scalars().first()
