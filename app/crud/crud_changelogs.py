from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.changelog import ChangeLog


def get_changelogs(db: Session, location_id: int) -> ChangeLog:
    return db.query(ChangeLog).filter(ChangeLog.location_id == location_id)\
        .order_by(desc(ChangeLog.created_at)).all()


