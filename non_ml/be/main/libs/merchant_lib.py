from sqlalchemy.ext.asyncio import AsyncSession

from main.schemas.merchant import AllMerchants, Merchant
from main.services import (
    merchant_service,
)


async def get_merchants(
    session: AsyncSession, page: int, per_page: int
) -> AllMerchants:
    merchants, count = await merchant_service.get_merchants(
        session=session, per_page=per_page, page=page
    )
    return AllMerchants(
        page=page,
        per_page=per_page,
        total=count,
        items=[Merchant.from_orm(merchant) for merchant in merchants],
    )
