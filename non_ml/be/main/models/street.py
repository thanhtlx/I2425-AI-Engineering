from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, TimestampMixin, DeleteMark
from .city import CityModel


class StreetModel(BaseModel, TimestampMixin, DeleteMark):
    __tablename__ = "streets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    city: Mapped["CityModel"] = relationship("CityModel", backref="streets")
