from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from src.utils import is_valid_integer
from conf import logger
from src.services.redis.storageTables import storage_colected_change_day
from src.keyboards import inline


async def cash_in_handler(message: types.Message, state: FSMContext):
    cash_in = message.text

    while is_valid_integer(cash_in):
        logger.info(f"cash in {cash_in}", message.chat.id)
        await state.update_data(change_cash_in=cash_in)
        await message.answer("please write total amount of spending")
        await storage_colected_change_day.change_cash_out.set()
        break
    else:
        await message.answer("please write total amount of sales with numbers")
        await storage_colected_change_day.change_cash_in.set()


async def cash_out_handler(message: types.Message, state: FSMContext):
    cash_out = message.text
    while is_valid_integer(cash_out):
        logger.info(f"cash in {cash_out}", message.chat.id)
        await state.update_data(change_cash_out=cash_out)

        data = await state.get_data()
        date_work = data.get("change_date_work")
        cash_in = data.get("change_cash_in")
        cash_out = data.get("change_cash_out")

        await message.answer(
            f"""
confirm that you filled correct information 
date_work: {date_work}   
cash_in: {cash_in}    
cash_out: {cash_out}
""", reply_markup=inline.CashBoxChangeDay()
        )

        break
    else:
        await message.answer("please write total amount of spending with numbers")
        await storage_colected_change_day.change_cash_out.set()


def register_message_handlers_cash_box_usm_update(dp: Dispatcher):
    dp.register_message_handler(cash_in_handler, state=storage_colected_change_day.change_cash_in)
    dp.register_message_handler(cash_out_handler, state=storage_colected_change_day.change_cash_out)
