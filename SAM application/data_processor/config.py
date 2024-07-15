import os

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_ENDPOINT = os.getenv("MYSQL_ENDPOINT")
MYSQL_PORT = os.getenv("MYSQL_PORT")
DB_NAME = os.getenv("DB_NAME")

ANSI_ENCODING = os.getenv("ANSI_ENCODING")
DATA_BUCKET = os.getenv("DATA_BUCKET")
DATA_PROCESSOR_STEP_FN = os.getenv("DATA_PROCESSOR_STEP_FN")

MYSQL_URL = (
    f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_ENDPOINT}:{MYSQL_PORT}/{DB_NAME}"
    if MYSQL_ENDPOINT
    else None
)
