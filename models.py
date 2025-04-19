from datetime import date, time
from sqlalchemy import String, Date, Time, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Earthquake(Base):
    __tablename__ = "earthquakes_myanmar_2025"

    id: Mapped[str] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    local_time: Mapped[time] = mapped_column(Time, nullable=False)
    place: Mapped[str] = mapped_column(nullable=False)
    magnitude: Mapped[float] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    depth_km: Mapped[float] = mapped_column(nullable=False)
    details: Mapped[str] = mapped_column(nullable=False)

