from datetime import datetime

from sqlalchemy import Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel, TimestampMixin, DeleteMark


class UserModel(BaseModel, TimestampMixin, DeleteMark):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dob: Mapped[datetime] = mapped_column(DateTime)
    gender: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    job: Mapped[str] = mapped_column(String(100))
    street_id: Mapped[int] = mapped_column(ForeignKey("streets.id"))
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    state_id: Mapped[int] = mapped_column(ForeignKey("states.id"))
    zip: Mapped[str] = mapped_column(String(50))
