# config.py
import os


class Config:
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "connect this to ur server"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
