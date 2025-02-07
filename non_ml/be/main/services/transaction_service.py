from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import select, func, Select
from sqlalchemy.ext.asyncio import AsyncSession

from main.models import (
    TransactionModel,
    UserModel,
    CityModel,
    StateModel,
    StreetModel,
    CreditCardModel,
    MerchantModel,
)
from main.schemas.transaction import TransactionQueryParams, FullDatasetTransactionData


def _apply_query_filter_from_params(
    stmt: Select[Any], params: TransactionQueryParams
) -> Select[Any]:
    if params.transaction_time_lower:
        stmt = stmt.where(
            TransactionModel.transaction_time >= params.transaction_time_lower
        )
    if params.transaction_time_upper:
        stmt = stmt.where(
            TransactionModel.transaction_time <= params.transaction_time_upper
        )
    if params.user_id:
        stmt = stmt.where(TransactionModel.user_id == params.user_id)
    if params.merchant_id:
        stmt = stmt.where(TransactionModel.merchant_id == params.merchant_id)
    if params.amount_lower:
        stmt = stmt.where(TransactionModel.amount >= params.amount_lower)
    if params.amount_upper:
        stmt = stmt.where(TransactionModel.amount <= params.amount_upper)
    if params.is_fraud is not None:
        stmt = stmt.where(TransactionModel.is_fraud == params.is_fraud)

    return stmt


async def get_transactions(
    session: AsyncSession, page: int, per_page: int, params: TransactionQueryParams
) -> tuple[list[TransactionModel], int]:
    stmt = select(TransactionModel)
    stmt = stmt.where(TransactionModel.is_deleted.is_(False))
    stmt = _apply_query_filter_from_params(stmt=stmt, params=params)

    # Count total number of rows (without pagination limit)
    count_stmt = select(func.count()).select_from(stmt.alias())
    count_result = await session.execute(count_stmt)

    # Fetch data with pagination
    stmt = stmt.limit(per_page).offset((page - 1) * per_page)
    result = await session.execute(stmt)
    return list(result.scalars().all()), count_result.scalar()


async def create_transaction(session: AsyncSession, data: dict) -> TransactionModel:
    transaction = TransactionModel(**data)
    session.add(transaction)
    await session.commit()
    return transaction


async def get_transaction(
    session: AsyncSession,
    transaction_id: int | None = None,
    transaction_number: str | None = None,
) -> TransactionModel | None:
    stmt = select(TransactionModel)
    if transaction_id:
        stmt = stmt.where(TransactionModel.id == transaction_id)
    if transaction_number:
        stmt = stmt.where(TransactionModel.transaction_number == transaction_number)
    stmt = stmt.where(TransactionModel.is_deleted.is_(False))
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_transactions_with_filters(
    session: AsyncSession, **kwargs
) -> list[TransactionModel]:
    stmt = select(TransactionModel)
    for key, value in kwargs.items():
        stmt = stmt.where(getattr(TransactionModel, key) == value)
    stmt = stmt.where(TransactionModel.is_deleted.is_(False))
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_transactions_between_date_mapping(
    session: AsyncSession, start_date: datetime, end_date: datetime
) -> dict[str, list[TransactionModel]]:
    stmt = (
        select(TransactionModel)
        .where(TransactionModel.transaction_time >= start_date)
        .where(TransactionModel.transaction_time <= end_date)
        .where(TransactionModel.exported_to_ml.is_(False))
    )
    stmt = stmt.where(TransactionModel.is_deleted.is_(False))
    result = await session.execute(stmt)

    # Init mapping with empty list
    return_mapping = {}
    current_date = start_date

    while current_date <= end_date:
        return_mapping[current_date.strftime("%d-%m-%Y")] = []
        current_date += timedelta(days=1)

    for transaction in list(result.scalars().all()):
        return_mapping[transaction.transaction_time.strftime("%d-%m-%Y")].append(
            transaction
        )
    return return_mapping


async def get_transactions_export_to_new_dataset(
    session: AsyncSession, start_date: datetime, end_date: datetime
) -> dict[str, list[FullDatasetTransactionData]]:
    stmt = (
        select(
            TransactionModel,
            UserModel,
            MerchantModel,
            StateModel,
            CityModel,
            StreetModel,
            CreditCardModel,
        )
        .join(UserModel, TransactionModel.user_id == UserModel.id)
        .join(StateModel, UserModel.state_id == StateModel.id)
        .join(CityModel, UserModel.city_id == CityModel.id)
        .join(StreetModel, UserModel.street_id == StreetModel.id)
        .join(CreditCardModel, TransactionModel.credit_card_id == CreditCardModel.id)
        .join(MerchantModel, TransactionModel.merchant_id == MerchantModel.id)
        .where(TransactionModel.transaction_time >= start_date)
        .where(TransactionModel.transaction_time <= end_date)
        .where(TransactionModel.exported_to_ml.is_(False))
    )
    stmt = (
        stmt.where(TransactionModel.is_deleted.is_(False))
        .where(UserModel.is_deleted.is_(False))
        .where(CityModel.is_deleted.is_(False))
        .where(StateModel.is_deleted.is_(False))
        .where(StreetModel.is_deleted.is_(False))
        .where(CreditCardModel.is_deleted.is_(False))
        .where(MerchantModel.is_deleted.is_(False))
    )
    result = await session.execute(stmt)

    final_result: dict[str, list[FullDatasetTransactionData]] = {}
    for transaction, user, merchant, state, city, street, credit_card in result.all():
        transaction_string_date = transaction.transaction_time.strftime("%d-%m-%Y")
        if transaction_string_date not in final_result:
            final_result[transaction_string_date] = []

        final_result[transaction_string_date].append(
            FullDatasetTransactionData(
                merchant=merchant.name,
                category=merchant.merchant_category,
                amt=transaction.amount,
                gender=user.gender,
                lat=transaction.coordination_metadata["user"]["latitude"],
                long=transaction.coordination_metadata["user"]["longitude"],
                city_pop=city.population,
                job=user.job,
                merch_lat=transaction.coordination_metadata["merchant"]["latitude"],
                merch_long=transaction.coordination_metadata["merchant"]["longitude"],
                trans_date_trans_time=transaction.transaction_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                unix_time=int(transaction.transaction_time.timestamp()),
                trans_num=transaction.transaction_number,
                dob=user.dob,
                city=city.name,
                state=state.name,
                zip=user.zip,
                street=street.name,
                cc_num=credit_card.number,
                last=user.last_name,
                first=user.first_name,
                is_fraud=transaction.is_fraud,
            )
        )

    return final_result
