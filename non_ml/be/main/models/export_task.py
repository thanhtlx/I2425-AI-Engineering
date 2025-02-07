from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel, TimestampMixin, DeleteMark


class ExportedTaskModel(BaseModel, TimestampMixin, DeleteMark):
    __tablename__ = "exported_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String(50))
    meta_data: Mapped[dict] = mapped_column(JSON, nullable=True)
