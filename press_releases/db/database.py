from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from press_releases.db.models import Source, Record, Base
from press_releases.logging_config import setup_logger

logger = setup_logger(__name__)


class Database:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        logger.info("Database initialized with URL: %s", db_url)

    def _get_session(self) -> Session:
        """Create and return a new SQLAlchemy session."""
        return self.Session()

    def add_channel(self, channel: Source) -> None:
        """Add a single channel to the database."""
        with self._get_session() as session:
            try:
                session.add(channel)
                session.commit()
                logger.info("Channel added: %s", channel.name)
            except Exception as e:
                session.rollback()
                logger.error("Error adding channel: %s", e)
                raise e

    def add_channels(self, channels: List[Source]) -> None:
        """Add multiple channels to the database, avoiding duplicates."""
        with self._get_session() as session:
            try:
                for channel in channels:
                    existing_channel = self.get_channel_by_name(channel.name, session)
                    if existing_channel is None:
                        session.add(channel)
                        logger.info("Channel added: %s", channel.name)
                session.commit()
            except Exception as e:
                session.rollback()
                logger.error("Error adding channels: %s", e)
                raise e

    def get_channel_by_id(self, channel_id: int, session: Optional[Session] = None) -> Optional[Source]:
        """Get a channel by its ID."""
        close_session = False
        if session is None:
            session = self._get_session()
            close_session = True
        try:
            channel = session.query(Source).filter_by(id=channel_id).first()
            logger.debug("Channel retrieved by ID %d: %s", channel_id, channel.name if channel else "None")
            return channel
        finally:
            if close_session:
                session.close()

    def get_channel_by_name(self, channel_name: str, session: Optional[Session] = None) -> Optional[Source]:
        """Get a channel by its name."""
        close_session = False
        if session is None:
            session = self._get_session()
            close_session = True
        try:
            channel = session.query(Source).filter_by(name=channel_name).first()
            logger.debug("Channel retrieved by name %s: %s", channel_name, channel.name if channel else "None")
            return channel
        finally:
            if close_session:
                session.close()

    def get_channels(self) -> List[Source]:
        """Get all channels."""
        with self._get_session() as session:
            channels = session.query(Source).all()
            logger.info("Retrieved %d channels", len(channels))
            return channels

    def add_record(self, record: Record) -> None:
        """Add a record to the database."""
        with self._get_session() as session:
            try:
                session.add(record)
                session.commit()
                logger.info("Record added: %s", record.title)
            except Exception as e:
                session.rollback()
                logger.error("Error adding record: %s", e)
                raise e

# Используйте конфигурацию из вашего файла настроек
# DATABASE_URL = f"postgresql://{cfg.DB_USER}:{cfg.DB_PASSWORD}@{cfg.DB_HOST}/{cfg.DB_NAME}"

DATABASE_URL = "sqlite:///press_rel.sqlite3"
db = Database(DATABASE_URL)
