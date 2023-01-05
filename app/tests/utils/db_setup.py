import os

from dotenv import load_dotenv


def get_url():
    load_dotenv()
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", 'admin')
    server = os.getenv("POSTGRES_SERVER", "localhost")
    db = "test_db"
    return f"postgresql://{user}:{password}@{server}/{db}"
