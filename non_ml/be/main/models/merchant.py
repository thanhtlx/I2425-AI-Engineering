from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel, TimestampMixin, DeleteMark


class MerchantModel(BaseModel, TimestampMixin, DeleteMark):
    __tablename__ = "merchants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    merchant_category: Mapped[str] = mapped_column(String(100))
