from datetime import timedelta, date


def day_of_week(date):
    days = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]
    day_nth = date.weekday()

    return days[day_nth]


def week_boundaries(year, week):
    start_of_year = date(year, 1, 1)
    now = start_of_year + timedelta(weeks=week)
    sun = now - timedelta(days=now.isoweekday() % 7)
    sat = sun + timedelta(days=6)

    return now, sat
