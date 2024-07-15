from environs import Env

env = Env()
env.read_env()

API_ID = env.str("API_ID")
API_HASH = env.str("API_HASH")

DB_NAME = env.str("DB_NAME", "press_releases")
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")

CHANNELS = env.list(
    "CHANNELS", ["news24kg", "kaktus_mediakg", "kloopnews", "akipress", "azattykrus"]
)
# CHANNELS = env.list("CHANNELS", ["news_handler"])
