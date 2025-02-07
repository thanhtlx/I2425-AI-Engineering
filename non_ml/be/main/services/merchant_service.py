from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from main.models import MerchantModel


async def get_merchants_by_ids(
    session: AsyncSession, ids: list[int]
) -> list[MerchantModel]:
    stmt = select(MerchantModel).where(MerchantModel.id.in_(ids))
    stmt = stmt.where(MerchantModel.is_deleted.is_(False))
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_merchant(session: AsyncSession, merchant_id: int) -> MerchantModel | None:
    stmt = select(MerchantModel).where(MerchantModel.id == merchant_id)
    stmt = stmt.where(MerchantModel.is_deleted.is_(False))
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_merchants(
    session: AsyncSession, page: int, per_page: int
) -> tuple[list[MerchantModel], int]:
    stmt = select(MerchantModel)
    stmt = stmt.where(MerchantModel.is_deleted.is_(False))

    count_stmt = select(func.count()).select_from(stmt.alias())
    count_result = await session.execute(count_stmt)

    result = await session.execute(stmt.limit(per_page).offset((page - 1) * per_page))
    return list(result.scalars().all()), count_result.scalar()
