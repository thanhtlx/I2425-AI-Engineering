from datetime import datetime

from pydantic import BaseModel, confloat

from main.models import (
    CreditCardModel,
    MerchantModel,
    UserModel,
    StreetModel,
    CityModel,
    StateModel,
)
from main.schemas.base import BasePaginationSchema
from main.schemas.common import Coordinate


class TransactionBase(BaseModel):
    id: int
    transaction_time: datetime
    credit_card_number: str
    merchant_name: str
    amount: float
    user_first_name: str
    user_last_name: str
    transaction_number: str
    is_fraud: bool | None


class AllTransactionsResponse(BasePaginationSchema):
    items: list[TransactionBase]


class TransactionDetail(TransactionBase):
    # unix_time: int
    merchant_latitude: float
    merchant_longitude: float
    user_gender: str
    user_street: str
    user_city: str
    user_state: str
    user_zip: str
    user_latitude: float
    user_longitude: float
    city_population: int
    user_dob: datetime
    merchant_category: str


class TransactionQueryParams(BaseModel):
    amount_lower: float | None = None
    amount_upper: float | None = None
    user_id: int | None = None
    merchant_id: int | None = None
    transaction_time_lower: datetime | None = None
    transaction_time_upper: datetime | None = None
    is_fraud: bool | None = None


class CreateTransactionRequest(BaseModel):
    transaction_time: datetime = datetime.utcnow()
    credit_card_id: int
    merchant_id: int
    amount: confloat(gt=0)
    user_id: int
    user_coordinate: Coordinate
    merchant_coordinate: Coordinate


class TransactionMLFlowFraudPrediction(BaseModel):
    merchant: str
    category: str
    amt: float
    gender: str
    lat: float
    long: float
    city_pop: int
    job: str
    unix_time: int
    merch_lat: float
    merch_long: float
    trans_date_trans_time: str


class FullDatasetTransactionData(TransactionMLFlowFraudPrediction):
    trans_num: str
    dob: datetime
    city_pop: int
    zip: str
    state: str
    city: str
    street: str
    last: str
    first: str
    cc_num: str
    is_fraud: bool


class ExportTransactionRequest(BaseModel):
    from_date: datetime
    to_date: datetime


class TransactionRelatedDataCreation:

    def __init__(
        self,
        credit_card: CreditCardModel,
        merchant: MerchantModel,
        user: UserModel,
        street: StreetModel,
        city: CityModel,
        state: StateModel,
    ):
        self.credit_card: CreditCardModel = credit_card
        self.merchant: MerchantModel = merchant
        self.user: UserModel = user
        self.street: StreetModel = street
        self.city: CityModel = city
        self.state: StateModel = state
