from dotenv import load_dotenv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.resolve().parent

load_dotenv()

DATABASES = {
    "sqlite3": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    "default": {
        "ENGINE": os.environ["POSTGRES_ENGINE"],
        "NAME": os.environ["POSTGRES_DB_NAME"],
        "USER": os.environ["POSTGRES_USER"],
        "HOST": os.environ["POSTGRES_HOST"],
        "POST": os.environ["POSTGRES_PORT"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
    },
}
