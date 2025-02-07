from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from main._db import get_db_session
from main.libs import merchant_lib
from main.schemas.merchant import AllMerchants

router: APIRouter = APIRouter()


@router.get("/merchants", response_model=AllMerchants)
async def get_merchants(
    session: AsyncSession = Depends(get_db_session),
    # _=Depends(get_principal),
    page: int = Query(1, ge=1),
    per_page: int = Query(1000, ge=1),
    # params: TransactionQueryParams = Depends(),
):
    all_merchants = await merchant_lib.get_merchants(
        session=session, page=page, per_page=per_page
    )
    return all_merchants
