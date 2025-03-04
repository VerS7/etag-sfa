"""
Constants
"""

from os import getenv, path


try:
    import dotenv

    env_file_path = path.join(path.dirname(__file__), ".env")

    if path.isfile(env_file_path):
        dotenv.load_dotenv(env_file_path)
    else:
        print("Can't find .env file. Env params loaded from system.")

except ModuleNotFoundError:
    print("Can't find python-dotenv package. Env params loaded from system.")

# App info
TITLE = "ETag-SFA Backend API"
DESCRIPTION = "## Backend API for ETag-SFA app"

# DB settings
DIALECT = "postgresql"
DRIVER = "asyncpg"

# DB access
USERNAME = getenv("DB_USERNAME")
PASSWORD = getenv("DB_PASSWORD")
URL = getenv("DB_URL")
DB_NAME = getenv("DB_NAME")

DB_CONN = f"{DIALECT}+{DRIVER}://{USERNAME}:{PASSWORD}@{URL}/{DB_NAME}"

# Admin access to backend
ADMIN_USERNAME = getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = getenv("ADMIN_PASSWORD")
