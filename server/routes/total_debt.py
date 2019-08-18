from flask import Blueprint, render_template
from server.db import Payed, get_data_of_date
from datetime import datetime, date, timedelta
from server.utils.datetime import week_boundaries


router = Blueprint('total_debt', __name__)

@router.route("/debt/total")
def render_total_debt_page():
    list_no = list(Payed.find({"payed": 0}))
    l = []
    weeks = {}
    for no in list_no:
        week = no['week']
        weeks[week] = 1
    result = []
    dates = {}
    for week, _ in weeks.items():
        if int(week) < 30:
            mon, sat = week_boundaries(2019, int(week))
        else:
            mon, sat = week_boundaries(2018, int(week))
        for d in [mon + timedelta(days=i) for i in range(0 - mon.weekday(), 7 - mon.weekday())]:
            dates[d] = 1
    for d, _ in dates.items():
        result += get_data_of_date(d.strftime("%Y-%m-%d"))
    # for r in result:
    #     print r
    for no in list_no:
        week = no['week']
        week_now = datetime.now().strftime("%U")
        if week == week_now:
            continue
        all = 0
        if week == "52":
            mon, sat = week_boundaries(2018, int(week))
        else:
            mon, sat = week_boundaries(2019, int(week))
        week = mon.strftime("%Y-%m-%d") + " den " + sat.strftime("%Y-%m-%d")
        if no['week'] == "52":
            no['week'] = "00"
        for r in result:
            if r['name'] == no['name']:
                if r['week'] == no['week']:
                    all += int(r['must_pay'])
        l.append(
            {"name": no['name'], "week": week, "must_pay": all, "_id": no['_id'], "start": mon.strftime("%Y-%m-%d")})
    return render_template("tongno.html", list_no=l)

