from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from main.models import CityModel


async def get_city(session: AsyncSession, city_id: int) -> CityModel | None:
    stmt = select(CityModel).where(CityModel.id == city_id)
    stmt = stmt.where(CityModel.is_deleted.is_(False))
    result = await session.execute(stmt)
    return result.scalars().first()
