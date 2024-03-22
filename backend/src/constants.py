"""
Constants
"""
from os import getenv, path


try:
    import dotenv

    env_file_path = ".env"

    if path.isfile(env_file_path):
        dotenv.load_dotenv(env_file_path)
    else:
        print("Can't find .env file. Env params loaded from system.")

except ModuleNotFoundError:
    print("Can't find python-dotenv package. Env params loaded from system.")


DIALECT = "postgresql"
DRIVER = "asyncpg"

USERNAME = getenv("DB_USERNAME")
PASSWORD = getenv("DB_PASSWORD")
URL = getenv("DB_URL")
DB_NAME = getenv("DB_NAME")

DB_CONN = f"{DIALECT}+{DRIVER}://{USERNAME}:{PASSWORD}@{URL}/{DB_NAME}"

ADMIN_USERNAME = getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = getenv("ADMIN_PASSWORD")
