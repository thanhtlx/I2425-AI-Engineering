# from sqlalchemy import Integer, String
# from sqlalchemy.orm import Mapped, mapped_column
#
# from .base import BaseModel, TimestampMixin, DeleteMark
#
#
# class JobModel(BaseModel, TimestampMixin, DeleteMark):
#     __tablename__ = "jobs"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     title: Mapped[str] = mapped_column(String(100))
