from dotenv import load_dotenv
import os

load_dotenv()

# REDIS
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = int(os.environ.get('REDIS_PORT'))
REDIS_DB = os.environ.get('REDIS_DB')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

# POSTGRES
POSTGRES_URL = os.environ.get('POSTGRES_STR')

# TELEGRAM
TOKEN = os.environ.get("BOT_TOKEN")

# USER_ID
Samvel = int(os.environ.get('SAMVEL'))
Armina = int(os.environ.get('ARMINA'))
Suren = int(os.environ.get('SUREN'))
Hayk = int(os.environ.get('HAYK'))

# WEBHOOKS

WEBHOOK_HOST = os.environ.get('WEBHOOK_HOST')
WEBHOOK_PORT = int(os.environ.get('WEBHOOK_PORT'))
WEBHOOK_DOMAIN = os.environ.get('WEBHOOK_DOMAIN')
