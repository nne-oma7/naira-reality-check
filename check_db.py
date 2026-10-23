
from database import SessionLocal
from models import PriceSnapshot

db = SessionLocal()

try:
    snapshots = (
        db.query(PriceSnapshot)
        .order_by(PriceSnapshot.id.desc())
        .limit(10)
        .all()
    )

    print(f"Total snapshots shown: {len(snapshots)}")

    for snapshot in snapshots:
        print(
            snapshot.id,
            snapshot.coin,
            snapshot.premium_percent,
            snapshot.recorded_at,
        )
finally:
    db.close()