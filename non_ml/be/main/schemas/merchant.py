from pydantic import BaseModel, ConfigDict

from main.schemas.base import BasePaginationSchema


class Merchant(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    merchant_category: str


class AllMerchants(BasePaginationSchema):
    items: list[Merchant]
