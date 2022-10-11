from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.changelog import ChangeLog


def create_changelog(db: Session, location_id: int, old_object: dict, new_object: dict):

    changelog = ChangeLog(
        location_id=location_id,
        action_type=1,
        old_flags=old_object,
        new_flags=new_object
    )

    db.add(changelog)
    db.commit()
    db.refresh(changelog)
    return changelog


def get_changelogs(db: Session, location_id: int) -> ChangeLog:
    return db.query(ChangeLog).filter(ChangeLog.location_id == location_id)\
        .order_by(desc(ChangeLog.created_at)).all()


