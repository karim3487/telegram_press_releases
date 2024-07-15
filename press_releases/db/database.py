from typing import List

from sqlalchemy import create_engine, Integer
from sqlalchemy.orm import sessionmaker

from press_releases.db.models import Source, Record, Base


class Database:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_channel(self, channel: Source) -> None:
        session = self.Session()
        session.add(channel)
        session.commit()
        session.close()

    def add_channels(self, channels: List[Source]) -> None:
        session = self.Session()
        for channel in channels:
            existing_channel = self.get_channel_by_name(channel.name)
            if existing_channel is None:
                session.add(channel)
        session.commit()
        session.close()

    def get_channel_by_id(self, channel_id: Integer) -> Source | None:
        session = self.Session()
        channel = session.query(Source).filter_by(id=channel_id).first()
        session.close()
        return channel

    def get_channel_by_name(self, channel_name: str) -> Source | None:
        session = self.Session()
        channel = session.query(Source).filter_by(name=channel_name).first()
        session.close()
        return channel

    def get_channels(self):
        session = self.Session()
        channels = session.query(Source).all()
        return channels

    def add_record(self, record: Record) -> None:
        session = self.Session()
        session.add(record)
        session.commit()
        session.close()


# DATABASE_URL = (
#     f"postgresql://{cfg.DB_USER}:{cfg.DB_PASSWORD}@{cfg.DB_HOST}/{cfg.DB_NAME}"
# )

DATABASE_URL = "sqlite:////Users/karimkabirov/PycharmProjects/work/telegram_press_releases/press_releases/press_rel.sqlite3"
db = Database(DATABASE_URL)
