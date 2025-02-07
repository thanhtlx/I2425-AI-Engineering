from main._db import get_db_session

from main.misc.utils.rest_client import RestAPIClient
from main.schemas.transaction import TransactionMLFlowFraudPrediction
from main.services import transaction_service, city_service


async def update_fraud_prediction_transactions(ml_model_path: str):
    from main.libs.log import get_logger

    logger = get_logger(__name__)
    async for session in get_db_session():
        try:
            unpredicted_transactions = (
                await transaction_service.get_transactions_with_filters(
                    session=session, is_fraud=None
                )
            )
            for transaction in unpredicted_transactions:
                # Load related data
                await session.refresh(transaction, ["customer", "merchant"])
                user = transaction.customer
                merchant = transaction.merchant
                city = await city_service.get_city(
                    session=session, city_id=user.city_id
                )

                # Coordinate data
                user_latitude = transaction.coordination_metadata["user"]["latitude"]
                user_longitude = transaction.coordination_metadata["user"]["longitude"]
                merchant_latitude = transaction.coordination_metadata["merchant"][
                    "latitude"
                ]
                merchant_longitude = transaction.coordination_metadata["merchant"][
                    "longitude"
                ]

                client = RestAPIClient(base_url=ml_model_path)
                predict_payload = TransactionMLFlowFraudPrediction(
                    merchant=merchant.name,
                    category=merchant.merchant_category,
                    amt=transaction.amount,
                    gender=user.gender,
                    lat=user_latitude,
                    long=user_longitude,
                    city_pop=city.population,
                    job=user.job,
                    merch_lat=merchant_latitude,
                    merch_long=merchant_longitude,
                    trans_date_trans_time=transaction.transaction_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    unix_time=int(transaction.transaction_time.timestamp()),
                )
                try:
                    response = await client.post(
                        "/predict", json={"data": predict_payload.model_dump()}
                    )
                except Exception as e:
                    logger.warning(
                        f"Error while calling ML pipeline: {e}, payload {predict_payload}"
                    )
                    return

                prediction = response.json().get("prediction", None)
                if prediction is not None:
                    transaction.is_fraud = bool(prediction)
                    await session.commit()
        finally:
            await session.close()
