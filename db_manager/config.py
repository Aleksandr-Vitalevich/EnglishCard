import os
from dotenv import load_dotenv

load_dotenv()

current_file_path = os.path.abspath(__file__)
db_manager_dir = os.path.dirname(current_file_path)

FILE_JSON_PATH = os.path.join(db_manager_dir, "words_first_data.json") 

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")