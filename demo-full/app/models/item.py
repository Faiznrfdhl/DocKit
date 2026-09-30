from sqlalchemy import Boolean, Column, Integer, String

from app.models.base import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)
    is_active = Column(Boolean, default=True)
