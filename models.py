
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String

from database import Base


class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    coin = Column(String, nullable=False, index=True)

    global_price_usd = Column(Float, nullable=False)
    usd_ngn_rate = Column(Float, nullable=False)
    global_implied_ngn = Column(Float, nullable=False)
    quidax_ngn = Column(Float, nullable=False)
    premium_percent = Column(Float, nullable=False)

    recorded_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )