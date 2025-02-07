from datetime import datetime

from sqlalchemy import Integer, DateTime, Float, ForeignKey, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import CreditCardModel
from .base import BaseModel, TimestampMixin, DeleteMark
from .merchant import MerchantModel
from .user import UserModel


class TransactionModel(BaseModel, TimestampMixin, DeleteMark):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaction_number: Mapped[str] = mapped_column(String(50))
    transaction_time: Mapped[datetime] = mapped_column(DateTime)
    is_fraud: Mapped[bool] = mapped_column(Integer, nullable=True)
    amount: Mapped[float] = mapped_column(Float)
    coordination_metadata: Mapped[dict] = mapped_column(JSON)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    merchant_id: Mapped[int] = mapped_column(ForeignKey("merchants.id"))
    credit_card_id: Mapped[int] = mapped_column(ForeignKey("credit_cards.id"))
    exported_to_ml: Mapped[bool] = mapped_column(Integer, default=False)
    customer: Mapped["UserModel"] = relationship(
        "UserModel", backref="transactions", lazy="raise"
    )
    merchant: Mapped["MerchantModel"] = relationship(
        "MerchantModel", backref="transactions", lazy="raise"
    )
    credit_card: Mapped["CreditCardModel"] = relationship(
        "CreditCardModel", backref="transactions", lazy="raise"
    )
