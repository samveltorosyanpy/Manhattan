from src.services.database.scheam.models import Session, select, desc, CashBox, and_, func
from typing import Any


class CashBoxTable():
    def __init__(self, logger):
        self.session = Session()
        self.logger = logger

    async def check_data(self, date_work):
        is_date_work = select(CashBox.date_work) \
            .where(CashBox.date_work == date_work)
        date_work = self.session.execute(is_date_work).scalar()

        return date_work

    async def new_day(
            self,
            date_work,
            cash_in: int,
            cash_out: int,
            user_id: int,
    ) -> Any:
        try:
            last_day_sum = select(CashBox.in_cash_box_sum) \
                .where(CashBox.date_work < date_work) \
                .order_by(desc(CashBox.date_work)) \
                .limit(1)

            last_day_sum = self.session.execute(last_day_sum).fetchone()
            last_day_sum = (0,) if last_day_sum is None else last_day_sum
            in_cash_box_sum = (cash_in + int(last_day_sum[0])) - cash_out

            data = CashBox(
                date_work=date_work,
                cash_in=cash_in,
                cash_out=cash_out,
                in_cash_box_sum=in_cash_box_sum
            )

            self.session.add(data)
            self.session.commit()
            self.logger.info(
                f'update cash box date_work={date_work}, cash_in={cash_in}, cash_out={cash_out}, in_cash_box_sum={in_cash_box_sum}',
                user_id)
            next_day = select(CashBox.date_work, CashBox.cash_in, CashBox.cash_out) \
                .where(CashBox.date_work > date_work) \
                .order_by(desc(CashBox.date_work))

            result = self.session.execute(next_day).fetchall()
            count_arr = len(result)
            for r in range(0, count_arr):
                count_arr -= 1
                last_total_sum = select(CashBox.in_cash_box_sum) \
                    .where(CashBox.date_work < result[count_arr][0]) \
                    .order_by(desc(CashBox.date_work))
                last_total_sum = self.session.execute(last_total_sum).fetchone()
                last_total_sum = (in_cash_box_sum,) if last_total_sum is None else last_total_sum

                new_sum = (last_total_sum[0] + result[count_arr][1]) - result[count_arr][2]

                update_cash_box_sum = self.session.query(CashBox) \
                    .where(CashBox.date_work == result[count_arr][0]) \
                    .order_by(desc(CashBox.date_work)).first()
                update_cash_box_sum.in_cash_box_sum = new_sum
                self.session.commit()
                self.logger.info(
                    f"date_work = {result[count_arr][0]} | ({last_total_sum[0]} + {result[count_arr][1]}) - {result[count_arr][2]} = {new_sum}",
                    user_id)

        except Exception as err:
            self.logger.error(err, user_id)

    async def change_shift_day(
            self,
            date_work,
            cash_in: int,
            cash_out: int,
            user_id: int,
    ) -> Any:
        last_day_sum = select(CashBox.in_cash_box_sum) \
            .where(CashBox.date_work < date_work) \
            .order_by(desc(CashBox.date_work)) \
            .limit(1)

        last_day_sum = self.session.execute(last_day_sum).fetchone()
        last_day_sum = (0,) if last_day_sum is None else last_day_sum
        in_cash_box_sum = (cash_in + int(last_day_sum[0])) - cash_out

        to_day = self.session.query(CashBox) \
                .where(CashBox.date_work == date_work) \
                .order_by(desc(CashBox.date_work)).first()
        to_day.cash_in = cash_in
        to_day.cash_out = cash_out
        to_day.in_cash_box_sum = in_cash_box_sum

        self.session.commit()

        self.logger.info(
            f'update cash box date_work={date_work}, cash_in={cash_in}, cash_out={cash_out}, in_cash_box_sum={in_cash_box_sum}',
            user_id)
        next_day = select(CashBox.date_work, CashBox.cash_in, CashBox.cash_out) \
            .where(CashBox.date_work > date_work) \
            .order_by(desc(CashBox.date_work))

        result = self.session.execute(next_day).fetchall()
        count_arr = len(result)
        for r in range(0, count_arr):
            count_arr -= 1
            last_total_sum = select(CashBox.in_cash_box_sum) \
                .where(CashBox.date_work < result[count_arr][0]) \
                .order_by(desc(CashBox.date_work))
            last_total_sum = self.session.execute(last_total_sum).fetchone()
            last_total_sum = (in_cash_box_sum,) if last_total_sum is None else last_total_sum

            new_sum = (last_total_sum[0] + result[count_arr][1]) - result[count_arr][2]

            update_cash_box_sum = self.session.query(CashBox) \
                .where(CashBox.date_work == result[count_arr][0]) \
                .order_by(desc(CashBox.date_work)).first()
            update_cash_box_sum.in_cash_box_sum = new_sum
            self.session.commit()
            self.logger.info(
                f"date_work = {result[count_arr][0]} | ({last_total_sum[0]} + {result[count_arr][1]}) - {result[count_arr][2]} = {new_sum}",
                user_id)

    async def report_with_interval(
            self,
            start_date,
            end_date,
    ) -> Any:
        report_data = select(func.sum(CashBox.cash_in), func.sum(CashBox.cash_out)).where(
            and_(CashBox.date_work >= start_date, CashBox.date_work <= end_date))
        row = self.session.execute(report_data).fetchone()

        return {'sales': row[0], 'spending': row[1]}
