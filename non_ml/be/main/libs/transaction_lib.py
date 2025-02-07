import csv
import io
from main.enums import TaskStatus
from main.libs.log import get_logger

from sqlalchemy.ext.asyncio import AsyncSession

from main import config
from main.misc.utils.rest_client import RestAPIClient
from main.misc.utils.string_utils import generate_random_hex_string
from main.models import TransactionModel
from main.models.export_task import ExportedTaskModel
from main.schemas.transaction import (
    AllTransactionsResponse,
    TransactionBase,
    CreateTransactionRequest,
    TransactionDetail,
    TransactionQueryParams,
    TransactionRelatedDataCreation,
    TransactionMLFlowFraudPrediction,
    ExportTransactionRequest,
    FullDatasetTransactionData,
)
from main.services import (
    transaction_service,
    merchant_service,
    credit_card_service,
    user_service,
    city_service,
    street_service,
    state_service,
    task_service,
    google_cloud_service,
)
from main.misc.exceptions import BadRequest, NotFound

logger = get_logger(__name__)


async def get_transactions(
    session: AsyncSession, page: int, per_page: int, params: TransactionQueryParams
) -> AllTransactionsResponse:
    transactions, count = await transaction_service.get_transactions(
        session=session, page=page, per_page=per_page, params=params
    )

    transaction_credit_card_ids = {
        transaction.credit_card_id for transaction in transactions
    }
    transaction_merchant_ids = {transaction.merchant_id for transaction in transactions}
    transaction_user_ids = {transaction.user_id for transaction in transactions}
    merchants = await merchant_service.get_merchants_by_ids(
        session=session, ids=list(transaction_merchant_ids)
    )
    credit_cards = await credit_card_service.get_credit_cards_by_ids(
        session=session, ids=list(transaction_credit_card_ids)
    )
    users = await user_service.get_users_by_ids(
        session=session, ids=list(transaction_user_ids)
    )

    transaction_credit_card_mapping = {
        credit_card.id: credit_card for credit_card in credit_cards
    }
    transaction_merchant_mapping = {merchant.id: merchant for merchant in merchants}
    transaction_user_mapping = {user.id: user for user in users}

    items = []
    for transaction in transactions:
        items.append(
            TransactionBase(
                id=transaction.id,
                transaction_time=transaction.transaction_time,
                credit_card_number=transaction_credit_card_mapping[
                    transaction.credit_card_id
                ].number,
                merchant_name=transaction_merchant_mapping[
                    transaction.merchant_id
                ].name,
                amount=transaction.amount,
                user_first_name=transaction_user_mapping[
                    transaction.user_id
                ].first_name,
                user_last_name=transaction_user_mapping[transaction.user_id].last_name,
                transaction_number=transaction.transaction_number,
                is_fraud=transaction.is_fraud,
            )
        )

    return AllTransactionsResponse(
        total=count, per_page=per_page, page=page, items=items
    )


async def _validate_transaction_data(
    session: AsyncSession, data: CreateTransactionRequest
):
    # Validation
    credit_card = await credit_card_service.get_credit_card(
        session=session, credit_card_id=data.credit_card_id
    )
    if not credit_card:
        raise BadRequest(
            error_message=f"Credit card with id {data.credit_card_id} not found"
        )

    if credit_card.owner_user_id != data.user_id:
        raise BadRequest(
            error_message=f"Credit card with id {data.credit_card_id} does not belong to user with id {data.user_id}"
        )

    merchant = await merchant_service.get_merchant(
        session=session, merchant_id=data.merchant_id
    )
    if not merchant:
        raise BadRequest(error_message=f"Merchant with id {data.merchant_id} not found")

    user = await user_service.get_user(session=session, user_id=data.user_id)
    if not user:
        raise BadRequest(error_message=f"User with id {data.user_id} not found")

    # Create transaction
    street = await street_service.get_street(session=session, street_id=user.street_id)
    city = await city_service.get_city(session=session, city_id=user.city_id)
    state = await state_service.get_state(session=session, state_id=user.state_id)
    assert street is not None
    assert state is not None
    assert city is not None

    return TransactionRelatedDataCreation(
        credit_card=credit_card,
        merchant=merchant,
        user=user,
        street=street,
        city=city,
        state=state,
    )


async def _is_transaction_potential_fraud(
    data: CreateTransactionRequest, related_data: TransactionRelatedDataCreation
) -> bool | None:
    # Call ML pipeline to evaluate fraud
    client = RestAPIClient(base_url=config.ML_MODEL_PATH)

    predict_payload = TransactionMLFlowFraudPrediction(
        merchant=related_data.merchant.name,
        category=related_data.merchant.merchant_category,
        amt=data.amount,
        gender=related_data.user.gender,
        lat=data.user_coordinate.latitude,
        long=data.user_coordinate.longitude,
        city_pop=related_data.city.population,
        job=related_data.user.job,
        merch_lat=data.merchant_coordinate.latitude,
        merch_long=data.merchant_coordinate.longitude,
        trans_date_trans_time=data.transaction_time.strftime("%Y-%m-%d %H:%M:%S"),
        unix_time=int(data.transaction_time.timestamp()),
    )
    try:
        response = await client.post("/predict", json=predict_payload.model_dump())
    except Exception as e:
        logger.warning(f"Error while calling ML pipeline: {e}")
        return None

    prediction = response.json().get("prediction", None)
    logger.info(f"Prediction: {prediction}, payload {str(predict_payload)}")
    if prediction is not None:
        prediction = bool(prediction)
    return prediction


async def validate_and_create_transaction(
    session: AsyncSession, data: CreateTransactionRequest
) -> TransactionDetail:
    transaction_related_data = await _validate_transaction_data(
        session=session, data=data
    )

    is_fraud = await _is_transaction_potential_fraud(
        data=data, related_data=transaction_related_data
    )

    transaction_create_data = {
        "transaction_number": generate_random_hex_string(),
        "transaction_time": data.transaction_time,
        "is_fraud": is_fraud,
        "amount": data.amount,
        "user_id": data.user_id,
        "merchant_id": data.merchant_id,
        "credit_card_id": data.credit_card_id,
        "coordination_metadata": {
            "user": {
                "latitude": data.user_coordinate.latitude,
                "longitude": data.user_coordinate.longitude,
            },
            "merchant": {
                "latitude": data.merchant_coordinate.latitude,
                "longitude": data.merchant_coordinate.longitude,
            },
        },
    }

    transaction = await transaction_service.create_transaction(
        session=session, data=transaction_create_data
    )
    return TransactionDetail(
        id=transaction.id,
        transaction_time=transaction.transaction_time,
        credit_card_number=transaction_related_data.credit_card.number,
        merchant_name=transaction_related_data.merchant.name,
        amount=transaction.amount,
        user_first_name=transaction_related_data.user.first_name,
        user_last_name=transaction_related_data.user.last_name,
        transaction_number=transaction.transaction_number,
        is_fraud=transaction.is_fraud,
        merchant_latitude=data.merchant_coordinate.latitude,
        merchant_longitude=data.merchant_coordinate.longitude,
        user_gender=transaction_related_data.user.gender,
        user_street=transaction_related_data.street.name,
        user_city=transaction_related_data.city.name,
        user_state=transaction_related_data.state.name,
        user_zip=transaction_related_data.user.zip,
        user_latitude=data.user_coordinate.latitude,
        user_longitude=data.user_coordinate.longitude,
        city_population=transaction_related_data.city.population,
        user_dob=transaction_related_data.user.dob,
        merchant_category=transaction_related_data.merchant.merchant_category,
    )


async def _synthesize_transaction_detail_data(
    session: AsyncSession, transaction: TransactionModel
) -> TransactionDetail:
    # Validation
    credit_card = await credit_card_service.get_credit_card(
        session=session, credit_card_id=transaction.credit_card_id
    )
    assert credit_card is not None

    assert credit_card.owner_user_id == transaction.user_id

    merchant = await merchant_service.get_merchant(
        session=session, merchant_id=transaction.merchant_id
    )
    assert merchant is not None

    user = await user_service.get_user(session=session, user_id=transaction.user_id)
    assert user is not None

    # Create transaction
    street = await street_service.get_street(session=session, street_id=user.street_id)
    city = await city_service.get_city(session=session, city_id=user.city_id)
    state = await state_service.get_state(session=session, state_id=user.state_id)
    assert street is not None
    assert state is not None
    assert city is not None

    return TransactionDetail(
        id=transaction.id,
        transaction_time=transaction.transaction_time,
        credit_card_number=credit_card.number,
        merchant_name=merchant.name,
        amount=transaction.amount,
        user_first_name=user.first_name,
        user_last_name=user.last_name,
        transaction_number=transaction.transaction_number,
        is_fraud=transaction.is_fraud,
        merchant_latitude=transaction.coordination_metadata["merchant"]["latitude"],
        merchant_longitude=transaction.coordination_metadata["merchant"]["longitude"],
        user_gender=user.gender,
        user_street=street.name,
        user_city=city.name,
        user_state=state.name,
        user_zip=user.zip,
        user_latitude=transaction.coordination_metadata["user"]["latitude"],
        user_longitude=transaction.coordination_metadata["user"]["longitude"],
        city_population=city.population,
        user_dob=user.dob,
        merchant_category=merchant.merchant_category,
    )


async def get_transaction_detail(
    session: AsyncSession,
    transaction_id: int | None = None,
    transaction_number: str | None = None,
) -> TransactionDetail | None:
    if transaction_number:
        # TODO: Complete this logic
        return None

    if transaction_id:
        # TODO: Check if match with owner OR admin user
        transaction = await transaction_service.get_transaction(
            session=session, transaction_id=transaction_id
        )
        if not transaction:
            raise NotFound(
                error_message=f"Transaction with id {transaction_id} not found"
            )

        return await _synthesize_transaction_detail_data(
            session=session, transaction=transaction
        )


def _export_to_in_memory_csv(data: list[dict]) -> io.StringIO:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    output.seek(0)
    return output


async def _set_task_fail(
    session: AsyncSession, task: ExportedTaskModel, error_metadata: dict
):
    task.status = TaskStatus.FAILED
    current_task_metadata = task.meta_data.copy()
    for key, value in error_metadata.items():
        current_task_metadata[key] = value
    task.meta_data = current_task_metadata
    await session.commit()


async def _trigger_build():
    client = RestAPIClient(base_url=config.TRIGGER_BUILD_URL)
    try:
        headers = {
            "Accept": config.TRIGGER_BUILD_ACCEPT,
            "Authorization": f"Bearer {config.TRIGGER_BUILD_TOKEN}",
        }
        json = {
            "ref": config.TRIGGER_BUILD_BRANCH,
            "inputs": {"reason": "Triggered via API"},
        }
        response = await client.post("/dispatches", json=json, headers=headers)
    except Exception as e:
        logger.warning(f"Error while trigger build: {e}")
        return str(e)

    return None


async def validate_latest_task(session: AsyncSession):
    latest_task = await task_service.get_latest_task(session=session)
    if latest_task and latest_task.status == TaskStatus.IN_PROGRESS:
        raise BadRequest(error_message="Another task is in progress")


def _update_task_progress_no_commit(task: ExportedTaskModel, progress: float):
    task_metadata = task.meta_data.copy()
    task_metadata["progress"] = progress
    task.meta_data = task_metadata


async def handle_export_data_and_build(
    session: AsyncSession, data: ExportTransactionRequest
):
    transactions: dict[str, list[FullDatasetTransactionData]] = (
        await transaction_service.get_transactions_export_to_new_dataset(
            session=session, start_date=data.from_date, end_date=data.to_date
        )
    )

    transaction_date_mapping = (
        await transaction_service.get_transactions_between_date_mapping(
            session=session, start_date=data.from_date, end_date=data.to_date
        )
    )

    task = await task_service.create_task(
        session=session,
        data={
            "status": TaskStatus.IN_PROGRESS,
            "meta_data": {
                "from_date": data.from_date.strftime("%d-%m-%Y"),
                "to_date": data.to_date.strftime("%d-%m-%Y"),
                "progress": 0,
            },
        },
    )

    for idx, key in enumerate(list(transactions.keys())):
        try:
            output = _export_to_in_memory_csv(
                data=[transaction.model_dump() for transaction in transactions[key]]
            )
            await google_cloud_service.upload_blob_from_memory(
                bucket_name=config.GCS_BUCKET_NAME,
                destination_blob_name=f"prediction/{key}/data.csv",
                contents=output.getvalue(),
            )
        except Exception as e:
            await _set_task_fail(
                session=session,
                task=task,
                error_metadata={"error": str(e), "error_date": key},
            )
            return

        for transaction in transaction_date_mapping[key]:
            transaction.exported_to_ml = True

        _update_task_progress_no_commit(
            task=task, progress=100 * (idx + 1) / len(list(transactions.keys()))
        )
        await session.commit()

    # Trigger build
    error = await _trigger_build()
    if error:
        await _set_task_fail(
            session=session, task=task, error_metadata={"error_build": error}
        )
        return

    task.status = TaskStatus.COMPLETED
    await session.commit()
