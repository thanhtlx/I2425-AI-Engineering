from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from main.models import StreetModel


async def get_street(session: AsyncSession, street_id: int) -> StreetModel | None:
    stmt = select(StreetModel).where(StreetModel.id == street_id)
    stmt = stmt.where(StreetModel.is_deleted.is_(False))
    result = await session.execute(stmt)
    return result.scalars().first()
