from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def CashBoxFunctions() -> InlineKeyboardMarkup:
    keybord = InlineKeyboardMarkup(row_width=1)
    but_1 = InlineKeyboardButton('Close the working day', callback_data='CashBox_CloseDay_work')
    but_2 = InlineKeyboardButton('Cash box total amount ☢️', callback_data='CashBox_ChangeShiftDay_change_shift_day')
    but_3 = InlineKeyboardButton('amount with interval', callback_data='CashBox_Report_sale_and_spending_with_interval')
    keybord.add(but_1, but_2, but_3)

    return keybord
