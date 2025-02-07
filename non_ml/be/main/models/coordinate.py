# from sqlalchemy import Integer, Float, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from .base import BaseModel, TimestampMixin, DeleteMark
# from .user import UserModel
#
#
# class CoordinateModel(BaseModel, TimestampMixin, DeleteMark):
#     __tablename__ = "coordinates"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     latitude: Mapped[float] = mapped_column(Float)
#     longitude: Mapped[float] = mapped_column(Float)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     user: Mapped["UserModel"] = relationship("UserModel", backref="coordinates")
