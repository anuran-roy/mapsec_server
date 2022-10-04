from tinydb import TinyDB
from main import BASE_DIR
import os

db_loc = str(BASE_DIR / "db.json")
db = TinyDB(db_loc)

if not os.path.exists(db_loc):
    os.system(f"touch {db_loc}")


def get_db():
    try:
        print("Accessing DB...")
        yield db
    finally:
        print("Database access complete.")
