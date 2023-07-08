from src.keyboards import inline
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from conf import logger, bot, ADMIN_ID, database_table_cash_box, SEND_DAY_MESSAGE
from src.services.redis.storageTables import storage_colected_change_day, storage_colected_new_work_day


async def CashBox_add_work_day(call: types.CallbackQuery, state: FSMContext) -> None:
    call_info = call.data.split('_')

    if call.data == 'CashBox_CloseDay_work':
        await call.message.answer('choose the date',
                                  reply_markup=inline.CashBoxAddShift.CashBoxCreateCalendarShiftDay())

    elif call_info[2] == 'DATE-CHANGE-MONTH':
        years, month = call_info[3:]
        logger.info(f'choose the date [ {years, month} ]', call.message.chat.id)
        await call.message.edit_reply_markup(
            reply_markup=inline.CashBoxAddShift.CashBoxCreateCalendarShiftDay(year=int(years), month=int(month)))

    elif call_info[2] == 'DateChoose':
        date_work = call_info[3]
        is_date_work_exist = await database_table_cash_box.check_data(date_work)

        if is_date_work_exist is None:
            logger.info(f'choose the date [ {date_work} ]', call.message.chat.id)
            await state.update_data(date_work=date_work)
            await call.message.answer('please write total sale amount')
            await storage_colected_new_work_day.cash_in.set()
        else:
            logger.info(f"shift date {date_work} is exist", call.message.chat.id)
            await call.message.answer('Working day is exist in table')

    elif call.data == 'CashBox_CloseDay_confirm_send_and_insert':
        data = await state.get_data()
        date_work = data.get("date_work")
        cash_in = data.get("cash_in")
        cash_out = data.get("cash_out")

        try:
            await call.message.edit_reply_markup(reply_markup=None)
        except Exception as err:
            logger.error(err, call.message.chat.id)
        await call.message.answer('Have a nice day 😊', reply_markup=inline.CashBoxOneMoireShiftDay())

        await database_table_cash_box.new_day(
            date_work=date_work,
            cash_in=int(cash_in),
            cash_out=int(cash_out),
            user_id=call.message.chat.id)

        for dies in SEND_DAY_MESSAGE:
            await bot.send_message(chat_id=dies, text=f"""
            closed shift in Manhattan
    date_work: {date_work}
    cash_in: {cash_in}
    cash_out: {cash_out}
    """)
        await state.finish()


    elif call.data == 'CashBox_CloseDay_cancel_send_and_insert':
        await call.message.answer('choose date', reply_markup=inline.CashBoxCreateCalendarShiftDay())
        await state.finish()

async def CashBox_change_sift_day(call: types.CallbackQuery, state: FSMContext) -> None:
    call_info = call.data.split('_')

    if call.data == 'CashBox_ChangeShiftDay_change_shift_day':
        await call.message.answer(
            'choose the date',
            reply_markup=inline.CashBoxCreateCalendarChangeShiftDay()
        )

    elif call_info[2] == 'DATE-CHANGE-MONTH':
        years, month = call_info[3:]
        logger.info(f'choose the date [ {years, month} ]', call.message.chat.id)
        await call.message.edit_reply_markup(
            reply_markup=inline.CashBoxCreateCalendarChangeShiftDay(year=int(years), month=int(month)))

    elif call_info[2] == 'DateChoose':
        date_work = call_info[3]

        logger.info(f'choose the date [ {date_work} ]', call.message.chat.id)
        await state.update_data(change_date_work=date_work)
        await call.message.answer('please write total sale amount')
        await storage_colected_change_day.change_cash_in.set()


    elif call.data == 'CashBox_ChangeShiftDay_confirm_change_day':
        data = await state.get_data()
        date_work = data.get("change_date_work")
        cash_in = data.get("change_cash_in")
        cash_out = data.get("change_cash_out")

        try:
            await call.message.edit_reply_markup(reply_markup=None)
        except Exception as err:
            logger.error(err, call.message.chat.id)

        await call.message.answer('Have a nice day 😊')

        await database_table_cash_box.change_shift_day(
            date_work=date_work,
            cash_in=int(cash_in),
            cash_out=int(cash_out),
            user_id=call.message.chat.id)

        await state.finish()


    elif call.data == 'CashBox_ChangeShiftDay_cancel_change_day':
        await call.message.answer('choose date', reply_markup=inline.CashBoxCreateCalendarChangeShiftDay())
        await state.finish()

async def CashBox_sales_and_spending_with_interval(call: types.CallbackQuery, state: FSMContext) -> None:
    call_info = call.data.split('_')

    if call.data == 'CashBox_Report_sale_and_spending_with_interval':
        await call.message.answer("@ntreq skzbi or@", reply_markup=inline.CashBoxReportStartDate())

    elif call_info[2] == 'START-DATE-CHANGE-MONTH':
        years, month = call_info[3:]
        logger.info(f'change the date moth [ {years, month} ]', call.message.chat.id)
        await call.message.edit_reply_markup(
            reply_markup=inline.CashBoxReportStartDate(year=int(years), month=int(month)))

    elif call_info[2] == 'StartDateChoose':
        start_date = call_info[3]
        await state.update_data(start_date=start_date)
        await call.message.edit_text(text="@ntreq verchin or@", reply_markup=inline.CashBoxReportEndDate())

    elif call_info[2] == 'END-DATE-CHANGE-MONTH':
        years, month = call_info[3:]
        logger.info(f'change the date moth [ {years, month} ]', call.message.chat.id)
        await call.message.edit_reply_markup(
            reply_markup=inline.CashBoxReportEndDate(year=int(years), month=int(month)))

    elif call_info[2] == 'EndDateChoose':
        await state.update_data(end_date=call_info[3])

        report_interval = await state.get_data()

        report_data = await database_table_cash_box.report_with_interval(
            report_interval.get('start_date'),
            report_interval.get('end_date')
        )

        await call.message.edit_text(text=f"""
                            date interval
{report_interval.get('start_date')} - {report_interval.get('end_date')}

sales:  {report_data.get('sales')}
spending:   {report_data.get('spending')}
""", reply_markup=None)
        await state.finish()


async def callback(call: types.CallbackQuery, state: FSMContext) -> None:
    logger.info(f'callback data {call.data}', call.message.chat.id)
    call_info = call.data.split('_')

    if call.data == 'cash_box_button':
        await call.message.answer('Cash box actions', reply_markup=inline.CashBox.CashBoxFunctions())

    elif call_info[0] == 'CashBox':

        if call_info[1] == 'CloseDay':
            await CashBox_add_work_day(call=call, state=state)

        if call_info[1] == 'ChangeShiftDay':
            await CashBox_change_sift_day(call=call, state=state)

        if call_info[1] == 'Report' and call.message.chat.id in ADMIN_ID:
            await CashBox_sales_and_spending_with_interval(call=call, state=state)


def register_message_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(callback, state='*')
