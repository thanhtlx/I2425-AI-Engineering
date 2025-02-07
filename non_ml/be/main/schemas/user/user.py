from datetime import datetime

from pydantic import BaseModel, ConfigDict

from main.schemas.base import BasePaginationSchema


class UserBase(BaseModel):
    id: int
    dob: datetime
    email: str
    first_name: str
    last_name: str
    gender: str


class AllUserResponse(BasePaginationSchema):
    items: list[UserBase]


class CreditCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    number: str


class UserDetail(UserBase):
    job: str
    street: str
    city: str
    state: str
    zip: str
    credit_cards: list[CreditCard] | None = None
