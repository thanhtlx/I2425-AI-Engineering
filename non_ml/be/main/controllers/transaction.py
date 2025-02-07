from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from main._db import get_db_session
from main.libs import transaction_lib
from main.schemas.transaction import (
    AllTransactionsResponse,
    TransactionDetail,
    CreateTransactionRequest,
    TransactionQueryParams,
    ExportTransactionRequest,
)

router: APIRouter = APIRouter()


@router.get("/transactions", response_model=AllTransactionsResponse)
async def get_transactions(
    session: AsyncSession = Depends(get_db_session),
    # _=Depends(get_principal),
    page: int = Query(1, ge=1),
    per_page: int = Query(1000, ge=1),
    params: TransactionQueryParams = Depends(),
):
    # TODO: Order by
    all_transactions: AllTransactionsResponse = await transaction_lib.get_transactions(
        session=session, per_page=per_page, page=page, params=params
    )
    return all_transactions


@router.get("/transactions/{transaction_id}", response_model=TransactionDetail)
async def get_transaction(
    transaction_id: int,
    session: AsyncSession = Depends(get_db_session),
    # _=Depends(get_principal),
):
    transaction_detail = await transaction_lib.get_transaction_detail(
        session=session, transaction_id=transaction_id
    )
    return transaction_detail


@router.post("/transaction", response_model=TransactionDetail)
async def create_transaction(
    data: CreateTransactionRequest,
    session: AsyncSession = Depends(get_db_session),
    # _=Depends(get_principal),
):
    return await transaction_lib.validate_and_create_transaction(
        session=session, data=data
    )


@router.post("/export-transactions")
async def export_transaction_data(
    data: ExportTransactionRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db_session),
):
    await transaction_lib.validate_latest_task(session)
    background_tasks.add_task(
        transaction_lib.handle_export_data_and_build, session, data
    )
    return {}
