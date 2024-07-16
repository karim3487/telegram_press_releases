import json
from pathlib import Path

from press_releases.db.database import db
from press_releases.db.models import Record
from telethon import TelegramClient, events
import config_reader as cfg
from logging_config import setup_logger
from press_releases.utils import log_new_message, extract_title_and_text_from_message, ensure_directory_exists, \
    add_channels_to_db, clean_message

logger = setup_logger(__name__)


async def message_handler(event: events.NewMessage.Event) -> None:
    """
    Handler for new messages in chats.

    :param event: Event object.
    """
    message = event.message
    chat = await event.get_chat()
    chat_username = chat.username

    json_msg = json.dumps(clean_message(message), ensure_ascii=False)

    log_new_message(message.chat.title, json_msg)

    if not message.message:
        return

    tg_channel_id = db.get_channel_by_name(chat_username).id
    link_to_record = f"https://t.me/{chat_username}/{message.id}"
    title, text = extract_title_and_text_from_message(message.message)

    record = Record(
        title=title,
        text=text,
        date_published=message.date,
        source_id=tg_channel_id,
        is_press_release=False,
        link_to_record=link_to_record,
    )

    try:
        db.add_record(record)
        logger.info(f"Processed message from {chat_username}. Message: {json_msg}")
    except Exception as e:
        logger.error(f"Failed to add record from {chat_username}. Error: {e}")


def setup_telegram_client(session_file: Path) -> TelegramClient:
    """
    Setup and return a configured Telegram client.

    :param session_file: Path to the session file.
    :return: Configured TelegramClient instance.
    """
    return TelegramClient(
        str(session_file),
        cfg.API_ID,
        cfg.API_HASH,
        system_version="4.16.30-vxCUSTOM",
    )


def main() -> None:
    session_dir = Path.cwd() / "telegram_sessions"
    ensure_directory_exists(session_dir)
    session_file = session_dir / "press_rel"

    client = setup_telegram_client(session_file)

    add_channels_to_db()

    client.add_event_handler(message_handler, events.NewMessage(chats=cfg.CHANNELS))

    with client:
        logger.info("Client started...")
        client.run_until_disconnected()


if __name__ == "__main__":
    main()
