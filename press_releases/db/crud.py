from sqlalchemy.orm import Session

from press_releases.db.database import Source


def create_channel(db: Session, name: str):
    db_item = Source(name=name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
