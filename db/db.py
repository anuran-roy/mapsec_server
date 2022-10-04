from tinydb import TinyDB
from main import BASE_DIR

db = TinyDB(str(BASE_DIR / "db.json"))


def get_db():
    try:
        print("Accessing DB...")
        yield db
    finally:
        print("Database access complete.")
