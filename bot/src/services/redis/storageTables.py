from aiogram.dispatcher.filters.state import State, StatesGroup


class storage_colected_new_work_day(StatesGroup):
    date_work = State()
    cash_in = State()
    cash_out = State()


class storage_colected_change_day(StatesGroup):
    change_date_work = State()
    change_cash_in = State()
    change_cash_out = State()


class storage_colected_report_interval(StatesGroup):
    start_date = State()
    end_date = State()
