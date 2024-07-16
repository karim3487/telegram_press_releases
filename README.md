# Telegram Press Releases Bot

This project is a Telegram bot that listens to specific channels and processes incoming messages to store them in a database. The bot extracts titles and text from messages, logs the information, and saves the records to a database. The project uses SQLAlchemy for database interactions and Telethon for interacting with the Telegram API.

---

## Features

- Listens to specific Telegram channels for new messages.
- Extracts and logs message titles and texts.
- Saves the processed messages into a database.
- Utilizes SQLAlchemy for database operations.
- Uses Telethon for Telegram API interactions.

## Requirements

- Python 3.7+
- PostgreSQL or SQLite
- Telegram API credentials

## Setup

### Using Poetry
This project uses Poetry for dependency management. To install Poetry, follow the official installation guide.

### Clone the Repository

```bash
git clone <<repository_url>>
cd telegram-press-releases
```

### Install Dependencies

```bash
 poetry install
```

### Configuration

Rename `env.example` on `.env` and modify values


### Database Setup
Make sure you have PostgreSQL or SQLite installed and configured. The database tables will be created automatically when you run the bot for the first time.

### Logging Configuration
Create a logging_config.py file in the root directory with the following content to set up logging:

```python
import logging
import sys

def setup_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(f"{name}.log")
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
```

### Running the Bot
To run the bot, use the following command:

```bash
poetry run python main.py
```