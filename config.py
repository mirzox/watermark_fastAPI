import os

from dotenv import load_dotenv

load_dotenv('.env')


class Config:
    TOKEN = os.environ.get("TOKEN")
    CHANNEL_ID = os.environ.get("CHANNEL_ID")
