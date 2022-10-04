from tinydb import TinyDB
from main import BASE_DIR
import os

db_loc = str(BASE_DIR / "db.json")
log_db_loc = str(BASE_DIR / "sync_data" / "log_db.json")


if not os.path.exists(db_loc):
    open(db_loc, "w").close()


if not os.path.exists(log_db_loc):
    os.makedirs(str(BASE_DIR / "sync_data"), exist_ok=True)
    open(log_db_loc, "w").close()

db = TinyDB(db_loc)
log_db = TinyDB(log_db_loc)


def get_db():
    try:
        print("Accessing DB...")
        yield db
    finally:
        print("Database access complete.")


def get_log_db():
    try:
        print("Accessing Log DB...")
        yield log_db
    finally:
        print("Log Database access complete.")
