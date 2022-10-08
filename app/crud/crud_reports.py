from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.models.reportoptions import ReportOption
from app.models.reports import Report


def create_report(db: Session, user_id: int, verbose_name: str, options: List[str]) -> Report:
    db_report = Report(verbose_name=verbose_name, created_by=user_id)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    for option in options:
        create_report_option(db, user_id, option, db_report.id)

    return db.query(Report).get(db_report.id).options(joinedload(Report.options))


def create_report_option(db: Session, user_id: int, verbose_name: str, report_id: int) -> ReportOption:
    db_option = ReportOption(created_by=user_id, verbose_name=verbose_name, report_id=report_id)
    db.add(db_option)
    db.commit()
    db.refresh(db_option)
    return db_option
