from pathlib import Path
from typing import Tuple, Optional

from telethon.tl.patched import Message

from press_releases.db.database import db
from press_releases.db.models import Source
from press_releases.logging_config import setup_logger
import config_reader as cfg

logger = setup_logger(__name__)


def ensure_directory_exists(directory_path: Path) -> None:
    """
    Ensure the specified directory exists. If not, create it.

    :param directory_path: Path to the directory to check/create.
    """
    try:
        directory_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory {directory_path} is ready.")
    except Exception as e:
        logger.error(
            f"An error occurred while creating the directory {directory_path}: {e}"
        )


def log_new_message(chat_username: str, message: str) -> None:
    """
    Log a new message from a chat.

    :param chat_username: The username of the chat.
    :param message: The message content.
    """
    logger.debug(f"New message in chat {chat_username}. Message: {message}")


def extract_title_and_text_from_message(message: str) -> Tuple[Optional[str], str]:
    """
    Extracts and returns the title and the remaining text from the message.

    :param message: The message content.
    :return: A tuple where the first element is the title (or None if no title is found),
             and the second element is the remaining text.
    """
    title, text = None, message
    if "\n" in message:
        title, text = message.split("\n", 1)
    elif "." in message:
        title, text = message.split(".", 1)

    if not text.strip():
        title, text = None, message

    return title, text


def add_channels_to_db() -> None:
    """
    Add configured channels to the database.
    """
    try:
        channels = [
            Source(name=name, link=f"https://t.me/{name}") for name in cfg.CHANNELS
        ]
        db.add_channels(channels)
        logger.info("Channels added to the database.")
    except Exception as e:
        logger.error(f"Failed to add channels to the database. Error: {e}")


def clean_message(message: Message) -> dict:
    c_msg = {
        "id": message.id,
        "username": message.chat.username,
        "text": message.message,
        "date": message.date.strftime("%d.%m.%Y, %H:%M:%S"),
        "media": message.media,
        "entities": message.entities,
        "url": f"https://t.me/{message.chat.username}/{message.id}",
    }
    return c_msg

