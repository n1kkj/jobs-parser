import os
from dotenv import load_dotenv

load_dotenv('.env')

BOT_TOKEN = os.getenv('BOT_TOKEN', '')

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_DB = int(os.getenv('REDIS_DB', 0))

REDIS_DATABASE_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

FILE_PATH = os.getenv('FILE_PATH', 'result.xlsx')
