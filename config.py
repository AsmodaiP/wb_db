import os

from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DATABASE = os.getenv('DATABASE')

DB_URI = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DATABASE}'
