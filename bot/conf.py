from src.services import Logger, CashBoxTable

import os
import datetime
from pyngrok import ngrok

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2


load_dotenv()

# REDIS DATABASE
storage = RedisStorage2(host=os.environ.get('REDIS_HOST'), port=int(os.environ.get('REDIS_PORT')),
                        db=os.environ.get('REDIS_DB'), password=os.environ.get('REDIS_PASSWORD'))

# BOT WEBHOOK

OWNER_BOT = 1357108258
ADMIN_ID = [1357108258, 636655056]
SEND_DAY_MESSAGE = [1279577233, 636655056, 1357108258]
STAFF = [325146197, 1357108258, 636655056]

# Samvel = 1357108258
# Armina = 1279577233
# suren = 636655056
# Lox = 325146197

TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(TOKEN)
Bot.set_current(bot)
dp = Dispatcher(bot, storage=storage)

webhook_path = f'/{TOKEN}'
webhook_host = os.environ.get('WEBHOOK_HOST')
webhook_port = int(os.environ.get('WEBHOOK_PORT'))

ngrok.conf.get_default().auth_token = os.environ.get('NGROK_AUT_TOKEN')
webhook_url = ngrok.connect(webhook_port).public_url
# LOGGER
dt = datetime.datetime.now().strftime("%Y-%m-%d")
log_dir = f"{os.path.dirname(os.path.abspath(__file__))}/src/services/LoggerService/logs/{dt}"

if os.path.exists(log_dir) is False:
    os.makedirs(log_dir)

logger = Logger('bot', f'{log_dir}/test.log')

# POSTGRES DATABASE
database_table_cash_box = CashBoxTable(logger)
