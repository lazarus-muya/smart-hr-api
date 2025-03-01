from dotenv import load_dotenv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.resolve().parent

load_dotenv()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    # "postgres": {
    #     "ENGINE": os.environ["POSTGRES_ENGINE"],
    #     "NAME": os.environ["POSTGRES_DB"],
    #     "USER": os.environ["POSTGRES_USER"],
    #     "HOST": os.environ["POSTGRES_HOST"],
    #     "POST": os.environ["DB_PORT"],
    #     "PASSWORD": os.environ["POSTGRES_PASSWORD"],
    # },
}
