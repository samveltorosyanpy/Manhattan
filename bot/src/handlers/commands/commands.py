from aiogram import types, Dispatcher
from src.keyboards import CashBoxButtons
from loader import logger


async def com_start(msg: types.Message) -> None:
    logger.info('command [ /admin ]', msg.chat.id)
    await msg.answer("Admin`s actions menu", reply_markup=CashBoxButtons())

async def com_help(msg: types.Message) -> None:
    logger.info('command [ /help ]', msg.chat.id)
    await msg.answer('welcome to Manhattan helper')

def register_command_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(com_start, commands=['admin'])

    dp.register_message_handler(com_help, commands=['help'])


