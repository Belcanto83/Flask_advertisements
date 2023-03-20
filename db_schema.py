from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


load_dotenv()

db = SQLAlchemy()

DSN = f'postgresql://{os.getenv("USER")}:{os.getenv("USER_PASSWORD")}@{os.getenv("DB_HOST")}:' \
      f'{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
