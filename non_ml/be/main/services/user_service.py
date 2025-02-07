from sqlalchemy.ext.asyncio import AsyncSession


from sqlalchemy import select, func

from main.models import CreditCardModel
from main.models.user import UserModel


async def get_user(session: AsyncSession, user_id: int) -> UserModel | None:
    stmt = select(UserModel).where(UserModel.id == user_id)
    stmt = stmt.where(UserModel.is_deleted.is_(False))
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_users_by_ids(session: AsyncSession, ids: list[int]) -> list[UserModel]:
    stmt = select(UserModel).where(UserModel.id.in_(ids))
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_users(
    session: AsyncSession, page: int, per_page: int
) -> tuple[list[UserModel], int]:
    stmt = select(UserModel)
    stmt = stmt.where(UserModel.is_deleted.is_(False))

    count_stmt = select(func.count()).select_from(stmt.alias())
    count_result = await session.execute(count_stmt)

    result = await session.execute(stmt.limit(per_page).offset((page - 1) * per_page))
    return list(result.scalars().all()), count_result.scalar()


async def get_user_credit_cards(
    session: AsyncSession, user_id: int
) -> list[CreditCardModel]:
    stmt = select(CreditCardModel).where(CreditCardModel.owner_user_id == user_id)
    stmt = stmt.where(CreditCardModel.is_deleted.is_(False))
    result = await session.execute(stmt)
    return list(result.scalars().all())
