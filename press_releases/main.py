from pathlib import Path
from typing import Union, Tuple, Optional

from press_releases.db.database import db
from press_releases.db.models import Source, Record
from telethon import TelegramClient, events

import config_reader as cfg
from logging_config import setup_logger

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
    if "\n" in message:
        title, text = message.split("\n", 1)
        if not text:
            title, text = None, message
    elif "." in message:
        title, text = message.split(".", 1)
        if not text:
            title, text = None, message
    else:
        title, text = None, message

    return title, text


async def message_handler(event: events.NewMessage.Event) -> None:
    """
    Handler for new messages in chats
    :param event: Event object.
    """

    message = event.message
    if not message.message:
        return

    chat_username = message.chat.username
    log_new_message(event.chat.title, message.message.replace("\n", "\\n"))

    tg_channel_id = db.get_channel_by_name(message.chat.username).id

    link_to_record = f"https://t.me/{message.chat.username}/{message.id}"
    title, text = extract_title_and_text_from_message(message.message)
    record = Record(
        title=title,
        text=text,
        date_published=message.date,
        source_id=tg_channel_id,
        is_press_release=False,
        link_to_record=link_to_record,
    )

    db.add_record(record)

    logger.info(f"Processed message from {chat_username}. Message: {message}")


session_dir = Path.cwd() / "telegram_sessions"
ensure_directory_exists(session_dir)
session_file = session_dir / "press_rel"

client = TelegramClient(
    str(session_file),
    cfg.API_ID,
    cfg.API_HASH,
    system_version="4.16.30-vxCUSTOM",
)

db.add_channels(
    [Source(name=name, link=f"https://t.me/{name}") for name in cfg.CHANNELS]
)

client.add_event_handler(
    message_handler,
    events.NewMessage(chats=cfg.CHANNELS),
)

with client:
    logger.info("Client started...")
    client.run_until_disconnected()
