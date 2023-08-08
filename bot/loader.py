from src.services import Logger, CashBoxTable

import os
import datetime
from pyngrok import ngrok
from data import config

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2


# REDIS DATABASE
storage = RedisStorage2(host=config.REDIS_HOST, port=config.REDIS_PORT,
                        db=config.REDIS_DB, password=config.REDIS_PASSWORD)

# BOT WEBHOOK

OWNER_BOT = config.Samvel
ADMIN_ID = [config.Samvel, config.Suren]
SEND_DAY_MESSAGE = [config.Suren, config.Samvel]
STAFF = [config.Samvel, config.Suren, config.Hayk]

TOKEN = config.TOKEN

bot = Bot(TOKEN)
Bot.set_current(bot)
dp = Dispatcher(bot, storage=storage)

ngrok.conf.get_default().auth_token = os.environ.get('NGROK_AUT_TOKEN')
webhook_url = ngrok.connect(config.WEBHOOK_PORT).public_url

# LOGGER
dt = datetime.datetime.now().strftime("%Y-%m-%d")
log_dir = f"{os.path.dirname(os.path.abspath(__file__))}/src/services/LoggerService/logs/{dt}"

if os.path.exists(log_dir) is False:
    os.makedirs(log_dir)

logger = Logger('bot', f'{log_dir}/test.log')

# POSTGRES DATABASE
database_table_cash_box = CashBoxTable(logger)
