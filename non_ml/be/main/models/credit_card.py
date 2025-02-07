from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, TimestampMixin, DeleteMark
from .user import UserModel


class CreditCardModel(BaseModel, TimestampMixin, DeleteMark):
    __tablename__ = "credit_cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String(50))
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner_user: Mapped["UserModel"] = relationship("UserModel", backref="credit_cards")
