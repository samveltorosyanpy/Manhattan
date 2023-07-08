from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def CashBoxButtons() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    but_1 = InlineKeyboardButton('cash box', callback_data='cash_box_button')
    keyboard.add(but_1)

    return keyboard