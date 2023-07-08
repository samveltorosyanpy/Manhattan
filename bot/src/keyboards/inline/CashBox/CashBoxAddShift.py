from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime, calendar

def CashBoxCreateCalendarShiftDay(year: int = None, month: int = None) -> InlineKeyboardMarkup:
    now = datetime.datetime.now()
    current_year = now.year if year is None else year
    current_month = now.month if month is None else month

    markup = InlineKeyboardMarkup(row_width=7)

    markup.add(*[InlineKeyboardButton(day, callback_data=f'IGNORE') for day in
                 ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']])

    first_day = datetime.datetime(current_year, current_month, 1)
    _, num_days = calendar.monthrange(current_year, current_month)

    days_added = 0
    for week in range(5):
        row = []
        for day in range(7):
            if days_added < num_days:
                date = first_day + datetime.timedelta(days=days_added)
                callback_data = f'CashBox_CloseDay_DateChoose_{date.strftime("%Y-%m-%d 00:00:00")}'
                row.append(InlineKeyboardButton(str(date.day), callback_data=callback_data))
                days_added += 1
            else:
                row.append(InlineKeyboardButton(" ", callback_data=f'IGNORE'))
        markup.row(*row)

    prev_month = current_month - 1 if current_month > 1 else 12
    prev_year = current_year if current_month > 1 else current_year - 1
    next_month = current_month + 1 if current_month < 12 else 1
    next_year = current_year if current_month < 12 else current_year + 1

    markup.row(
        InlineKeyboardButton('<<', callback_data=f'CashBox_CloseDay_DATE-CHANGE-MONTH_{prev_year}_{prev_month}'),
        InlineKeyboardButton(f"{first_day.strftime('%Y-%m')}", callback_data=f'IGNORE'),
        InlineKeyboardButton('>>', callback_data=f'CashBox_CloseDay_DATE-CHANGE-MONTH_{next_year}_{next_month}')
    )

    return markup


def CashBoxSendAndInsert() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    but_1 = InlineKeyboardButton('confirm', callback_data='CashBox_CloseDay_confirm_send_and_insert')
    but_2 = InlineKeyboardButton('cancel', callback_data='CashBox_CloseDay_cancel_send_and_insert')

    keyboard.add(but_1, but_2)

    return keyboard


def CashBoxOneMoireShiftDay() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    but_1 = InlineKeyboardButton('One more', callback_data='CashBox_CloseDay_work')

    keyboard.add(but_1)

    return keyboard





