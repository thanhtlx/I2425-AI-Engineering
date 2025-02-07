from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, TimestampMixin, DeleteMark
from .state import StateModel


class CityModel(BaseModel, TimestampMixin, DeleteMark):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    population: Mapped[int] = mapped_column(Integer)
    state_id: Mapped[int] = mapped_column(ForeignKey("states.id"))
    state: Mapped["StateModel"] = relationship("StateModel", backref="cities")
