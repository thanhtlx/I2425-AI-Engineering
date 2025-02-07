from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from main.models import CreditCardModel


async def get_credit_cards_by_ids(
    session: AsyncSession, ids: list[int]
) -> list[CreditCardModel]:
    stmt = select(CreditCardModel).where(CreditCardModel.id.in_(ids))
    stmt = stmt.where(CreditCardModel.is_deleted.is_(False))
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_credit_card(
    session: AsyncSession, credit_card_id: int
) -> CreditCardModel | None:
    stmt = select(CreditCardModel).where(CreditCardModel.id == credit_card_id)
    stmt = stmt.where(CreditCardModel.is_deleted.is_(False))
    result = await session.execute(stmt)
    return result.scalars().first()
