from datetime import timedelta

import holidays

def calculate_working_days(start_date, end_date):
    if not start_date or not end_date:
        return 0

    if end_date < start_date:
        return 0

    years = range(start_date.year, end_date.year + 1)

    bank_holidays = holidays.UnitedKingdom(
        years=years,
        subdiv="ENG"
    )

    working_days = 0
    current_day = start_date

    while current_day <= end_date:
        is_weekday = current_day.weekday() < 5
        is_bank_holiday = current_day in bank_holidays

        if is_weekday and not is_bank_holiday:
            working_days += 1

        current_day += timedelta(days=1)

    return working_days
