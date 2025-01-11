from datetime import datetime, date
from sqlalchemy import Integer, String, func
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy.sql.sqltypes import DateTime, Date


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(16), nullable=False)
    birthday: Mapped[date] = mapped_column(Date, nullable=True)
    info: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column("created_at", DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column("updated_at", DateTime, default=func.now(), onupdate=func.now())
